### Struktur
* Om du siktar på G behöver du bara GP-datan i 'data'-mappen. 
* Extradatan för VG-uppgifterna finns i mappen 'data_vg_gemma' eller 'data_vg_lagerlof', beroende på vilken option du väljer. 


### Översättning och Taggning
* Datan är automatisk översatt med [OPUS](https://aclanthology.org/2020.eamt-1.61/). 
* Datan är taggat med SpaCy modellen [’sv_core_news_lg’](https://spacy.io/models/sv).
Den här taggaren använder UPOS taggar som skiljer sig lite grann från taggarna i labbarna.
Se [dokumentationen](https://universaldependencies.org/u/pos/) för mer information.
Obs att den automatiska taggningen inte är perfekt, speciellt för dialogkorpuserna som skiljer sig ganska mycket från taggarens träningsdata. 
