from modeltranslation.translator import translator, TranslationOptions
from profile.models import Instrument, Interest, Region, Genre


class InstrumentTranslationOptions(TranslationOptions):
    fields = ('name',)


class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)


class InterestTranslationOptions(TranslationOptions):
    fields = ('name',)


class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Instrument, InstrumentTranslationOptions)
translator.register(Genre, GenreTranslationOptions)
translator.register(Interest, InterestTranslationOptions)
translator.register(Region, RegionTranslationOptions)