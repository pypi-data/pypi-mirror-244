from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


def get_vocab_term(context, field, value):
    """Get vocab term dict for context, field ,value
    returns: {'token': token, 'title': title}
    """
    vocab_term = {
        "token": None,
        "title": None,
    }
    vocab_term["token"] = value
    vocab_name = field.vocabularyName
    factory = getUtility(IVocabularyFactory, vocab_name)
    if not factory:
        return vocab_term

    # collective.taxonomy support:
    if hasattr(factory, "translate"):
        vocab_term["title"] = get_taxonomy_vocab_title(
            context,
            factory,
            value,
        )
    elif IVocabularyFactory.providedBy(factory):
        vocab_term["title"] = get_vocab_title(
            context,
            factory,
            value,
        )
    return vocab_term


def get_taxonomy_vocab_title(context, factory, value):
    vocab_title = factory.translate(
        value,
        context=context,
    )
    return vocab_title


def get_vocab_title(context, factory, value):
    vocab = factory(context)
    vocab_title = vocab.getTerm(value).title
    return vocab_title
