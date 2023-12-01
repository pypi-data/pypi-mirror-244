import inspect
import json
import os.path

import time
import traceback

from sqapi.request import Get
from sqapi.api import SQAPI, DEFAULT_HOST
from sqapi.media import SQMediaObject

DEFAULT_PROB_THRESH = 0.5
DEFAULT_POLL_DELAY = -1
DEFAULT_ANNOTATOR_NAME = '{user[first_name]}-{user[last_name]}'


class Annotator:
    def __init__(self, host: str = DEFAULT_HOST, api_key: str = None, annotator_info: str = None,
                 prob_thresh: float = DEFAULT_PROB_THRESH, poll_delay: int = DEFAULT_POLL_DELAY,
                 label_map_file: str = None, verbosity: int = 2, email_results: bool = None,
                 non_supplementary: bool = False, **kw):
        """
        Generic annotator abstract class

        :param annotator_info: used for the name of the annotation_set, include version info, defaults to ClassName
        :param label_map_file: path to a local file that contains the label mappings
        :param prob_thresh: probability threshold for submitted labels, only submitted if p > prob_thresh
        :param poll_delay: the poll delay for running the loop (in seconds). To run once, set poll_delay = -1 (default)
        :param annotation_set_id: if supplied, will create suggested labels to the specific annotation_set with that ID
        :param affiliation_group_id: if supplied, will attempt to annotate all annotation_sets within an affiliation group
        :param user_group_id: if supplied, will attempt to annotate all annotation_sets within a user_group
        :param after_date: filter annotation_sets that were created after a specific date
        :param host: the Squidle+ instance hostname
        :param api_key: the API key for the user on that `host`. If omitted, you'll be prompted to log in.
        :param verbosity: the verbosity of the output (0,1,2,3)
        :param email_results: flag to optionally send an email upon completion
        :param non_supplementary: flag to optionally label directly without creating a supplementary set (with suggestions)
        """
        annotator_info = annotator_info or self.__class__.__name__
        self.sqapi = SQAPI(host=host, api_key=api_key, verbosity=verbosity)
        self.annotator_info = annotator_info.format(user=self.sqapi.current_user)  #(annotator_name or self.sqapi.cliargs.annotator_name).format(user=self.sqapi.current_user)
        self.prob_thresh = prob_thresh #or self.sqapi.cliargs.prob_thresh
        self.poll_delay = poll_delay #or self.sqapi.cliargs.poll_delay
        self.label_map_file = label_map_file #or self.sqapi.cliargs.label_map_file
        self.email_results = email_results
        self.non_supplementary = non_supplementary
        self.labels = []
        self.label2id = None

    def start(self, annotation_set_request: Get):
        """

        :param annotation_set_request:
        :return:
        """
        while True:
            self.run(annotation_set_request)
            if isinstance(self.poll_delay, (float, int)) and self.poll_delay > 0:
                time.sleep(self.poll_delay)
            else:
                break

    def run(self, annotation_set_request: Get, page=1, results_per_page=200, email_results=None):
        """

        :param annotation_set_request:
        :param page:
        :param results_per_page:
        :param email_results:
        :return:
        """
        annotation_sets = annotation_set_request.page(page).results_per_page(results_per_page).execute().json()

        print(f"\nFOUND: {annotation_sets.get('num_results')} annotation_sets | processing page {annotation_sets.get('page')}/{annotation_sets.get('total_pages')}...\n")

        # process current page of annotation_sets
        i = 0
        for a in annotation_sets.get("objects"):
            try:
                i += 1
                print(f"{'*'*80}\nProcessing ANNOTATION_SET: {(annotation_sets.get('page')-1)*results_per_page+i} / {annotation_sets.get('num_results')} | ID:{a.get('id')} > {a.get('name')} [{a.get('user',{}).get('username')}] ...\n{'*'*80}\n")
                media_count, point_count, annotation_count = self.process_annotation_set(a)
                if self.email_results if email_results is None else email_results:
                    self.email_annotation_set_user(a, media_count, point_count, annotation_count)
            except Exception as e:
                print(traceback.format_exc())

        # paginate annotation_sets, if more than one page returned
        if annotation_sets.get("page") < annotation_sets.get("total_pages"):
            self.run(annotation_set_request=annotation_set_request, page=page+1, results_per_page=results_per_page, email_results=email_results)

    def process_annotation_set(self, original_annotation_set):
        """

        :param original_annotation_set:
        :return:
        """
        self.code2label = self.get_label_mappings(original_annotation_set)
        if self.non_supplementary:
            annotation_set = original_annotation_set
        else:
            annotation_set = self.create_supplemental_annotation_set(parent_data=original_annotation_set)
        media_count, point_count, annotation_count = self.annotate_media_list(annotation_set)
        return media_count, point_count, annotation_count

    def get_label_mappings(self, annotatation_set_data):
        """

        :param annotatation_set_data:
        :return:
        """
        assert os.path.isfile(self.label_map_file), \
            f"label_map_file '{self.label_map_file}' does not appear to be a valid file. A Label Mapping file is required"


        label_scheme_id = annotatation_set_data.get("label_scheme", {}).get("id")
        label_scheme_data = self.sqapi.get(f"/api/label_scheme/{label_scheme_id}").execute().json()
        parent_label_scheme_ids = label_scheme_data.get("parent_label_scheme_ids")
        with open(self.label_map_file) as f:
            label_map_filters = json.load(f)
        if isinstance(label_map_filters, dict):
            code2label = {}
            for l, filts in label_map_filters.items():
                code2label[l] = self.get_label(filts, parent_label_scheme_ids)
        elif isinstance(label_map_filters, list):
            code2label = []
            for filts in label_map_filters:
                code2label.append(self.get_label(filts, parent_label_scheme_ids))
        else:
            raise TypeError("Unknown `label_map_filters` type. Must be a `list` or a `dict`")

        return code2label

    def get_label(self, filts, label_scheme_ids:list):
        """

        :param filts:
        :param label_scheme_ids:
        :return:
        """
        if isinstance(filts, list):
            r = self.sqapi.get("/api/label", single=True).filters_and(filts)
            r.filter(name="label_scheme_id", op="in", val=label_scheme_ids)
            return r.execute().json()
        return None

    def create_supplemental_annotation_set(self, parent_data, child_name=None, child_description=None):
        """

        :param parent_data:
        :param child_name:
        :param child_description:
        :return:
        """
        child_data = dict()
        child_data["user_id"] = self.sqapi.current_user.get("id")
        child_data['media_collection_id'] = parent_data.get("media_collection",{}).get("id")
        child_data['label_scheme_id'] = parent_data.get('label_scheme',{}).get('id')
        child_data['parent_id'] = parent_data.get('id')
        child_data['description'] = child_description or "Suggested annotations by '{}' for the '{}' annotation_set." \
                              "This is not a standalone annotation set.".format(self.annotator_info, parent_data.get("name"))
        child_data['name'] = child_name or self.annotator_info

        return self.sqapi.post("/api/annotation_set", json_data=child_data).execute().json()

    def create_annotation_label(self, code, likelihood=0.0, tag_names=None, comment=None, needs_review=False):
        if code is not None:
            label = self.code2label[code]  # if dict, use key, otherwise treat as index to list

            # build up annotations list
            if label is not None:
                return dict(
                    label_id=label.get("id"),
                    likelihood=float(likelihood),
                    tag_names=tag_names,
                    comment=comment,
                    needs_review=needs_review
                )
        return None

    def create_annotation_label_point_px(self, code, likelihood=0.0, tag_names=None, comment=None, needs_review=False,
                                         row=None, col=None, width=None, height=None, polygon=None, t=None):
        return dict(
            pixels=dict(row=row, col=col, width=width, height=height, polygon=polygon),
            annotation_label=self.create_annotation_label(
                code=code, likelihood=likelihood, tag_names=tag_names, comment=comment, needs_review=needs_review
            ),
            t=t
        )

    def annotate_media_list(self, annotation_set_data, page=1, results_per_page=500):
        """

        :param annotation_set_data:
        :param page:
        :param results_per_page:
        :return:
        """
        annotation_set_id = annotation_set_data.get("id")
        media_collection_id = annotation_set_data.get("media_collection",{}).get("id")
        # media_list =self.get_media_collection_media(media_collection_id, page=page, results_per_page=results_per_page)
        media_list = self.sqapi.get("/api/media", page=page, results_per_page=results_per_page).filter(
            name="media_collections", op="any", val=dict(name="id", op="eq", val=media_collection_id)
        ).order_by(field="timestamp_start", direction="asc").execute().json()
        num_results = media_list.get('num_results')
        media_count = point_count = annotation_count = 0

        for m in media_list.get("objects"):
            media_count += 1
            print(f"\nProcessing: media item {media_count + (page-1)*results_per_page} / {num_results}")
            media_url = m.get('path_best')
            media_type = m.get("media_type", {}).get("name")
            mediaobj = SQMediaObject(media_url, media_type=media_type, media_id=m.get('id'))

            # get media annotations. If this frame has not been observed, it will generat the annotations through the request
            base_annotation_set_id = annotation_set_data.get("parent_id") or annotation_set_data.get("id")
            media_annotations = self.sqapi.get(f"/api/media/{m.get('id')}/annotations/{base_annotation_set_id}").execute().json()
            points = media_annotations.get('annotations')
            point_count += len(points)

            # run point predictions
            annotations = []
            for p in points:
                self.process_point(p, mediaobj, annotation_set_id)
                annotation_count += 1

            # Submit any detected points through to annotation_set
            new_points = self.detect_points(mediaobj)
            for p in new_points:
                p['annotation_set_id'] = base_annotation_set_id
                p['media_id'] = mediaobj.id
                if isinstance(p.get('annotation_label'), dict):
                    p['annotation_label']['annotation_set_id'] = annotation_set_id
                self.sqapi.post("/api/point", json_data=p).execute()

        # continue until all images are processed
        if media_list.get("page") < media_list.get("total_pages"):
            _mc, _pc, _ac = self.annotate_media_list(
                annotation_set_data, page=page+1, results_per_page=results_per_page)
            media_count += _mc
            point_count += _pc
            annotation_count += _ac

        return media_count, point_count, annotation_count

    def process_point(self, point, mediaobj, annotation_set_id):
        point_id = point.get("id")
        x = point.get('x')
        y = point.get('y')
        t = point.get('t')

        # decide whether a point label or a frame label
        if x is not None and y is not None:
            a = self.classify_point(mediaobj, x=x, y=y, t=t)
        else:
            a = self.classify_frame(mediaobj, t=t)

        # print(f"code: {code}, prob: {probability}")
        # time.sleep(1)

        if not isinstance(a, dict) and isinstance(a, tuple) and len(a) == 2:
            code, likelihood = a
            # lookup label_id from classifier code. If dict, use get, otherwise assume list index code
            a = self.create_annotation_label(code, likelihood=likelihood)
        if a is not None:
            a.update(dict(
                user_id=self.sqapi.current_user.get("id"),
                annotation_set_id=annotation_set_id,
                point_id=point_id
            ))
            # Submit and save any new annotations
            if a.get('likelihood', 0) >= self.prob_thresh:
                self.sqapi.post("/api/annotation", json_data=a).execute()

    def email_annotation_set_user(self, a, media_count, point_count, annotation_count):
        user_ids = [a.get('user', {}).get('id')]
        annotation_set_url = "{}/geodata/annotation_set/{}".format(self.sqapi.host, a.get("id"))
        message = f'Hi {a.get("user", {}).get("first_name")}, <br><br>\n' \
                  f'Your annotation set "<b>{a.get("media_collection", {}).get("name")} >> {a.get("name")}</b>" has been ' \
                  f'processed by {self.annotator_info}. {media_count} media items were analysed, including {point_count} points and ' \
                  f'{annotation_count} annotations. Any Label suggestions will appear as "Magical Suggestions".<br><br>\n' \
                  f'To see results, click: <a href="{annotation_set_url}">{annotation_set_url}</a>'
        self.sqapi.send_user_email("SQ+ BOT: your Annotation Set has been processed", message, user_ids=user_ids)

    def classify_point(self, mediaobj: SQMediaObject, x, y, t):
        """

        :param mediaobj:
        :param x:
        :param y:
        :param t:
        :return:
        """
        print(f"classifying point media_url: {mediaobj.url}\nx: {x}\ny: {y}\nt: {t}")
        return self.create_annotation_label(code=None, likelihood=0)

    def classify_frame(self, mediaobj: SQMediaObject, t):
        """

        :param mediaobj:
        :param t:
        :return:
        """
        print(f"classifying frame media_url: {mediaobj.url}\nt: {t}")
        return self.create_annotation_label(code=None, likelihood=0)

    def detect_points(self, mediaobj: SQMediaObject):
        """

        :param mediaobj:
        :return:
        """
        print(f"detecting points media_url: {mediaobj.url}")
        # return a list of
        # self.create_annotation_label_point_px(classifier_code, prob, row=row, col=col, width=mediaobj.width, height=mediaobj.height)
        # or for polygon
        # self.create_annotation_label_point_px(classifier_code, prob, polygon=polygon, width=mediaobj.width, height=mediaobj.height)
        return []





