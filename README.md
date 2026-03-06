# Next tasks to implement (priorities):

1. Upgrade TermDistribution. Enable defining plots for related words. User can specify how many most related words to include. Related words can be verified by LLM before plotting.

2. (RelationFinder) Input: subject (e.g., Poland), predicate (e.g., enemy), object (e.g., Russia); find fragments which mention defined triples. Predicate and object can be empty, but subject is required.

If predicate is empty find all fragments which mention subject and object in relation and define all relations. User then can click and filterby relation.

If object is empty find all fragments which mention subject and predicate in relation and define all objects. User then can click and filter by object.

# Masters Thesis: "The analysis of Russian strategic communication 2000-2024 using Natural Language Processing" repository
Thesis Author: Grzegorz Zbrzeżny

Thesis Supervisor: dr Anna Wróblewska


## List of research questions created by author of this repository in collaboration with Ernest Wyciszkiewicz and Centrum Dialogu im. Juliusza Mieroszewskiego.

#### Original list of questions in Polish:

STATYSTYKA
* Ile razy w całej bazie występują słowa „Polska”, „Ukraina”, …? (TaskTermCount)
* W których latach Putin najczęściej wspominał o ….? (TaskTermDistribution)
* Jakie państwo, poza Rosją, pojawia się najczęściej w przemówieniach? (TaskTermCount)
* Jakie trzy pojęcia związane z gospodarką pojawiają się najczęściej? (RelatedTermCounts)
* Ile razy w kontekście militarnym występuje słowo „modernizacja”? (RelationFinder)
* W ilu wystąpieniach pojawia się słowo „demokracja”? (TaskTermCount)
* Jak często mówi o „przyjaźni” w stosunku do Chin? (RelationFinder)
* W których latach pojawia się najwięcej odniesień do II wojny światowej (RelatedTermCounts)


KONTEKST
* W jakim kontekście najczęściej pojawia się „Polska”? (wróg, partner, sojusznik, sąsiad) (TermRelationIdentifier)
* Jak Putin charakteryzuje USA – bardziej jako zagrożenie czy potencjalnego partnera? (TermRelationIdentifier)
* Jakie określenia najczęściej towarzyszą słowu „Ukraina”? (TermMentionIdentifier)
* Jakie metafory Putin stosuje wobec USA, Ukrainy, Polski i Niemiec? (?)
* Czy w odniesieniach do Polski częściej występują konteksty historyczne czy współczesne? (TimelineIdentifier)
* Czy Rosja częściej opisywana jest jako „ofiara”, „lider”, czy „obrońca”? (TermRelationIdentifier)


ZMIANA W CZASIE
* Jak zmienia się obraz Ukrainy (*Polski, Niemiec, USA) w przemówieniach od 2000 do 2024 roku? (?)
* Kiedy zaczynają się pojawiać liczne odniesienia do „ruskiego miru”? (?)
* Jak często wspomina o rozszerzeniu NATO – przed 2004 i po 2004 roku? (?)
* Kiedy zaczynają dominować wątki o „suwerenności”  w polityce zagranicznej? (TermMentionIdentifier)
* Jak często mówi o „zagrożeniu” przed i po 2014 roku? (TaskTermDistribution)
* W których latach najczęściej występują wątki związane z gospodarką? (TermMentionIdentifier)
* W którym momencie Putin zaczyna mówić o „wielobiegunowym świecie”? (TermMentionIdentifier)


PORÓWNANIE
* Jak różni się narracja wobec Polski i Niemiec? (?)
* Czy o USA mówi tym samym językiem co o NATO? (?)
* Jakie wątki historyczne pojawiają się w odniesieniu do Ukrainy, a jakie do Gruzji? (?)
* Czy częściej mówi pozytywnie o Chinach niż o Indiach? (?)
* Jak zmienia się ton wypowiedzi wobec USA w porównaniu z Unią Europejską? (?)
* Jak różni się obraz Niemiec w latach 2003 (wojna w Iraku) i 2014 (kryzys ukraiński)? (?)


INTERPRETACJE
* Jakie są najczęściej powtarzające się argumenty Putina za umacnianiem armii? (?)
* Jak konstruuje obraz „wroga”? (?)
* Jakie wydarzenia historyczne służą mu jako legitymizacja działań wobec Ukrainy? (?)
* W jaki sposób używa narracji o „zwycięstwie w II wojnie światowej”? (?)
* Jakie elementy mitu o „wielkiej Rosji” powtarzają się w jego wystąpieniach? (?)
* Jakie są trzy główne sposoby opisywania Zachodu? (?)
* Jak Putin łączy wątki historyczne z aktualną polityką zagraniczną? (?)
* W jaki sposób mówi o „zagrożeniu” w celu mobilizacji społecznej? (?)
* Jakie motywy religijne pojawiają się w jego przemówieniach? (?)
* Jak przedstawia rolę Rosji w świecie – jako mocarstwa obronnego czy ekspansywnego? (?)


#### Questions translated to English:

STATISTICS
* How many times do the words “Poland”, “Ukraine”, … appear in the entire database? (TaskTermCount)
* In which years did Putin most often mention …? 
* Which country, apart from Russia, appears most frequently in his speeches?
* Which three economy-related terms appear most often? 
* How many times does the word “modernization” appear in a military context?
* In how many speeches does the word “democracy” appear?
* How often does he speak about “friendship” in relation to China?
* In which years do the most references to World War II occur?

CONTEXT
* In what context does “Poland” most often appear? (enemy, partner, ally, neighbor)
* How does Putin characterize the USA – more as a threat or as a potential partner?
* What adjectives or terms most often accompany the word “Ukraine”?
* What metaphors does Putin use toward the USA, Ukraine, Poland, and Germany?
* In references to Poland, are historical or contemporary contexts more frequent?
* Is Russia more often described as a “victim”, a “leader”, or a “defender”?

CHANGE OVER TIME
* How does the image of Ukraine (Poland, Germany, USA) change in his speeches from 2000 to 2024?
* When do numerous references to the “Russian world” (russkiy mir) begin to appear?
* How often does he mention NATO expansion – before and after 2004?
* When do themes of “sovereignty” begin to dominate foreign policy discourse?
* How often does he speak about “threats” before and after 2014?
* In which years do economic topics appear most frequently?
* At what point does Putin start talking about a “multipolar world”?

COMPARISON
* How does the narrative toward Poland differ from that toward Germany?
* Does he speak about the USA in the same terms as about NATO?
* What historical themes appear in relation to Ukraine, and which in relation to Georgia?
* Does he speak more positively about China than about India?
* How does the tone toward the USA compare with that toward the European Union?
* How does the image of Germany differ between 2003 (Iraq War) and 2014 (Ukraine crisis)?

INTERPRETATIONS
* What are Putin’s most common arguments for strengthening the army?
* How does he construct the image of the “enemy”?
* What historical events does he use to legitimize actions toward Ukraine?
* How does he employ the narrative of “victory in World War II”?
* What elements of the “Great Russia” myth recur in his speeches?
* What are the three main ways he describes the West?
* How does Putin connect historical themes with current foreign policy?
* How does he speak about “threats” to mobilize society?
* What religious motifs appear in his speeches?
* How does he portray Russia’s role in the world – as a defensive or expansionist power?
