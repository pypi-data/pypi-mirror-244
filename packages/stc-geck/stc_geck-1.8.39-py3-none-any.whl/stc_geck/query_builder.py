from typing import (
    Dict,
    List,
    Optional,
)

from .advices import PR_TEMPORAL_RANKING_FORMULA, default_term_field_mapper_configs, default_field_aliases, \
    default_field_boosts


class IndexQueryBuilder:

    def __init__(
        self,
        index_alias: str,
        scorer_function,
        snippet_configs: Optional[Dict] = None,
        is_fieldnorms_scoring_enabled: bool = False,
        exact_matches_promoter: Optional[Dict] = None,
        term_field_mapper_configs: Optional[Dict] = None,
    ):
        self.index_alias = index_alias
        self.scorer_function = scorer_function
        self.snippet_configs = snippet_configs
        self.is_fieldnorms_scoring_enabled = is_fieldnorms_scoring_enabled
        self.exact_matches_promoter = exact_matches_promoter
        self.term_field_mapper_configs = term_field_mapper_configs

    @staticmethod
    def from_profile(index_alias: str, profile: str):
        match profile:
            case 'light':
                return IndexQueryBuilder(
                    index_alias=index_alias,
                    scorer_function=None,
                    snippet_configs={
                        'title': 1024,
                        'abstract': 140,
                    },
                    is_fieldnorms_scoring_enabled=False,
                    exact_matches_promoter=None,
                    term_field_mapper_configs=default_term_field_mapper_configs
                )
            case 'full':
                return IndexQueryBuilder(
                    index_alias=index_alias,
                    scorer_function={'eval_expr': PR_TEMPORAL_RANKING_FORMULA},
                    snippet_configs={
                        'title': 1024,
                        'abstract': 140,
                    },
                    is_fieldnorms_scoring_enabled=True,
                    exact_matches_promoter={
                        'slop': 0,
                        'boost': 2.0,
                        'fields': ['abstract', 'extra', 'title']
                    },
                    term_field_mapper_configs=default_term_field_mapper_configs
                )
            case _:
                raise ValueError('incorrect profile')

    def build(
        self,
        query: dict,
        limit: int,
        offset: int,
        is_fieldnorms_scoring_enabled: Optional[bool] = None,
        collector: str = 'top_docs',
        fields: Optional[List[str]] = None,
        skip_doi_isbn_term_field_mapper: bool = False,
        query_language: str = 'en'
    ):
        query_parser_config = {
            'query_language': query_language,
            'term_limit': 20,
            'field_aliases': default_field_aliases,
            'field_boosts': default_field_boosts,
        }

        if self.exact_matches_promoter:
            query_parser_config['exact_matches_promoter'] = self.exact_matches_promoter

        if self.term_field_mapper_configs:
            term_field_mapper_configs = self.term_field_mapper_configs
            if skip_doi_isbn_term_field_mapper and 'doi_isbn' in self.term_field_mapper_configs:
                term_field_mapper_configs = dict(term_field_mapper_configs)
                term_field_mapper_configs.pop('doi_isbn', None)
            query_parser_config['term_field_mapper_configs'] = term_field_mapper_configs
        query_struct['match']['query_parser_config'] = query_parser_config
        collector_struct = {
            'limit': limit,
        }
        if collector == 'top_docs':
            if scorer := self.scorer_function:
                collector_struct['scorer'] = scorer
            if self.snippet_configs:
                collector_struct['snippet_configs'] = self.snippet_configs
            if offset:
                collector_struct['offset'] = offset
        if fields:
            collector_struct['fields'] = fields
        return {
            'index_alias': self.index_alias,
            'query': query,
            'collectors': [
                {collector: collector_struct},
                {'count': {}}
            ],
            'is_fieldnorms_scoring_enabled': (
                is_fieldnorms_scoring_enabled
                if is_fieldnorms_scoring_enabled is not None
                else self.is_fieldnorms_scoring_enabled
            ),
        }
