from enum import Enum
from typing import Dict, List, Optional, Set

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from pymusas.lexicon_collection import LexiconCollection
from pymusas.pos_mapper import UPOS_TO_USAS_CORE
from pymusas.spacy_api.taggers import rule_based  # noqa: F401
import spacy


lang_model_name = {
    'dutch': 'nl_core_news_sm',
    'french': 'fr_core_news_sm',
    'italian': 'it_core_news_sm',
    'portuguese': 'pt_core_news_sm',
    'spanish': 'es_core_news_sm',
    'chinese': 'zh_core_web_sm'
}

spacy_lang_exclude = {
    'nl_core_news_sm': ['parser', 'ner', 'tagger'],
    'fr_core_news_sm': ['parser', 'ner'],
    'it_core_news_sm': ['parser', 'ner', 'tagger'],
    'pt_core_news_sm': ['parser', 'ner'],
    'es_core_news_sm': ['parser', 'ner'],
    'zh_core_web_sm': ['parser', 'ner']
}


spacy_lang_model: Dict[str, spacy.language.Language] = {}

spacy_lang_tags: Dict[str, List[str]] = {
    'nl_core_news_sm': ['text', 'lemma_', 'pos_', '_.usas_tags'],
    'fr_core_news_sm': ['text', 'lemma_', 'pos_', '_.usas_tags'],
    'it_core_news_sm': ['text', 'lemma_', 'pos_', '_.usas_tags'],
    'pt_core_news_sm': ['text', 'lemma_', 'pos_', '_.usas_tags'],
    'es_core_news_sm': ['text', 'lemma_', 'pos_', '_.usas_tags'],
    'zh_core_web_sm': ['text', 'pos_', '_.usas_tags']
}

spacy_lang_lexicon_url: Dict[str, str] = {
    'nl_core_news_sm': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Dutch/semantic_lexicon_dut.tsv',
    'fr_core_news_sm': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.tsv',
    'it_core_news_sm': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Italian/semantic_lexicon_ita.tsv',
    'pt_core_news_sm': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/semantic_lexicon_pt.tsv',
    'es_core_news_sm': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Spanish/semantic_lexicon_es.tsv',
    'zh_core_web_sm': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Chinese/semantic_lexicon_chi.tsv'
}


def load_spacy_models() -> None:
    for lang, exclude in spacy_lang_exclude.items():
        nlp = spacy.load(lang, exclude=exclude)
        usas_tagger: rule_based.USASRuleBasedTagger = nlp.add_pipe('usas_tagger')
        spacy_lang_model[lang] = nlp
        # Rule based tagger requires a USAS lexicon
        usas_lexicon_url = spacy_lang_lexicon_url[lang]
        # Includes the POS information
        lexicon_lookup = LexiconCollection.from_tsv(usas_lexicon_url)
        # excludes the POS information
        lemma_lexicon_lookup = LexiconCollection.from_tsv(usas_lexicon_url,
                                                          include_pos=False)
        # Add the lexicon information to the USAS tagger within the pipeline
        usas_tagger.lexicon_lookup = lexicon_lookup
        usas_tagger.lemma_lexicon_lookup = lemma_lexicon_lookup
        # Maps from the POS model tagset to the lexicon POS tagset
        usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
    

load_spacy_models()


class SupportedLanguages(str, Enum):
    dutch = "dutch"
    french = "french"
    italian = "italian"
    portuguese = "portuguese"
    spanish = "spanish"
    chinese = "chinese"


class SpacyToken(BaseModel):
    text: str = Field(..., description="Token text", example="Cars")
    lemma: Optional[str] = Field(None, description="Lemma of token", example="car")
    pos: str = Field(..., description="Part Of Speech (POS) tag of token", example="noun")
    usas_tags: List[str] = Field(...,
                                 description=("List of USAS tags of the token in "
                                              "rank order, the most likely tag is "
                                              "the first tag in the list, in the "
                                              "example the most likely tag is `Z1`."),
                                 example=["Z1", "Z2"])


def spacy_processing(model_name: str, text: str) -> List[SpacyToken]:
    nlp = spacy_lang_model[model_name]
    tokens: List[SpacyToken] = []
    for token in nlp(text):
        text = token.text
        lemma = token.lemma_ if token.lemma_ else None
        pos = token.pos_
        usas_tags = token._.usas_tags
        tokens.append(SpacyToken(text=text, lemma=lemma, pos=pos, usas_tags=usas_tags))
    return tokens


app = FastAPI()


@app.get("/", response_model=List[SpacyToken], tags=['Tagging'],
         summary="Tags the text.",
         response_description='An array of `SpacyToken`s.')
async def tag(lang: SupportedLanguages = Query(...,
                                               description='Language of the text.'),
              text: str = Query(..., description='Text to be tagged.')
              ) -> List[SpacyToken]:
    '''
    Tokenises, lemmatises (for all languages but Chinese), Part Of Speech tags,
    and semantic tags (with USAS tags) the text returning this information as a
    an array of `SpacyToken`s. The `lang` should be the language of the text
    and this determines the model that is used.

    All but the semantic tags are the output of the small version of the
    pre-trained spaCy model for the given language, the semantic tags are the
    output of the given language PyMUSAS model. For example for French it uses
    the [small French spaCy model](https://spacy.io/models/fr#fr_core_news_sm)
    and the [French PyMUSAS model](https://ucrel.github.io/pymusas/usage/how_to/tag_text#french).
    '''
    model_name = lang_model_name[lang.value]
    return spacy_processing(model_name, text)


@app.get("/supported-languages", response_model=Set[SupportedLanguages], tags=['Tagging'],
         summary="Outputs all languages the tagger supports.",
         response_description="An array of languages the tagger supports.")
async def supported_languages() -> Set[SupportedLanguages]:
    return {language for language in SupportedLanguages}
