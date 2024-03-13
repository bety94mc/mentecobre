var orders = [
  "Corredores del Viento",
  "Rompedores del Cielo",
  "Portadores del Polvo",
  "Danzantes del Filo",
  "Vigilantes de la Verdad",
  "Tejedores de Luz",
  "Nominadores de lo Otro",
  "Escultores de Voluntad",
  "Custodios de Piedra",
  "Forjadores de Vínculos"
];

var Windrunner = 0;
var Skybreaker = 1;
var Dustbringer = 2;
var Edgedancer = 3;
var Truthwatcher = 4;
var Lightweaver = 5;
var Elsecaller = 6;
var Willshaper = 7;
var Stoneward = 8;
var Bondsmith = 9;

var orderData = [
  {
    name: "Corredores del Viento",
    color: "#0f3562",
    textColor: "#FFFFFF",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/01_windrunner_placard.jpg",
    catchphrase: "Protegeré",
    herald: "Jezerezeh",
    archetype: "Rey",
    gemstone: "zafiro",
    oathTheme:
      "Los juramentos de los Corredores del Viento giran en torno a la protección, en particular la defensa de los inocentes o de aquellos incapaces de protegerse a sí mismos.",
    role:
      "Los Corredores del Viento tienden a atraer al tipo de personas «hermanos mayores», que buscan proteger a los indefensos, pero que también disfrutan con la acción y que luchan por aquello en lo que creen. Básicamente son exploradores, aunque a menudo también trabajan como grupos de fuerzas especiales, capaces de llevar grupos de Radiantes tras las líneas enemigas en misiones secretas. Tienden a ser el tipo más convencional de soldados, creyendo en las estructuras de mando, las dinámicas de grupos, y la importancia de un escuadrón de hermanos y hermanas. A menudo tienen un número de escuderos mayor que el de las demás Órdenes, y se centran más en ser maestros de sus armas que ninguna otra Orden.",
    power1: "Adhesión",
    power1Desc: "unir cosas",
    power2: "Gravitación",
    power2Desc:
      "cambiar la dirección y la fuerza de la atracción gravitatoria sobre un objeto, tú incluido, lo que básicamente te otorga el poder de volar.",
    blogName: "Corredores del Viento",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Corredores_del_Viento"
  },
  {
    name: "Rompedores del Cielo",
    color: "#5f5d68",
    textColor: "#FFFFFF",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/02_skybreaker_placard.jpg",
    catchphrase: "Buscaré justicia",
    herald: "Nalan",
    archetype: "Juez",
    gemstone: "Cuarzo ahumado",
    oathTheme:
      " Los juramentos de los Rompedores del Cielo giran en torno a la protección, luchar por causas justas, y reforzar las normas sociales. Por lo general, refuerzan la importancia de los códigos morales, las estructuras legales, y condiciones semejantes que protegen la civilización.",
    role:
      "Los Rompedores del Cielo fueron los responsables del cumplimiento de las leyes de los Caballeros Radiantes, encargados a menudo de mantener la paz, vigilando a las demás Órdenes, y asegurándose de que ciertas fuerzas peligrosas de la oscuridad fueran contenidas en el mundo. En ocasiones, esto les ganó una mala reputación entre aquellas Órdenes de caballeros Radiantes con un pensamiento más libre, pero los Rompedores del Cielo (en su mayoría) no eran despiadados. Eran los que creían que nadie, ni siquiera un Radiante, debía estar por encima de ser cuestionado. Fueron los que llevaban a cabo la, ocasionalmente, dura tarea de asegurarse de que ciertas Órdenes no abusaran de sus poderes, convirtiéndose en tiranos, ya que los Rompedores del Cielo veían que aquellos con poderes podían oprimir fácilmente a quienes no tenían ninguno. <br/> Tienden a atraer a quienes creen en la importancia del código legal, a aquellos con fuertes códigos morales propios, y a quienes piensan que la mejor defensa contra la anarquía son cosas como el patriotismo, la fibra moral, y las normas para gobernar el comportamiento. Tened en cuenta que en su encarnación actual, guiada por el Heraldo Nale en su locura, la Orden es más rígida que la antigua, que entendía que la ley no era perfecta, pero que representaba un ideal que alcanzar con el tiempo. Cualquiera que crea en encontrar la justicia verdadera, en defender a los inocentes, y castigar al culpable sería bien recibido en la orden.",
    power1: "Gravitación",
    power1Desc: " cambiar la dirección y la fuerza de la atracción gravitatoria sobre un objeto, tú incluido, lo que básicamente te otorga el poder de volar",
    power2: "División",
    power2Desc: " manipular el ritmo al que algo se descompone",
    blogName: "Rompedores del Cielo",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Rompedores_del_Cielo"
  },
  {
    name: "Portadores del Polvo",
    color: "#b02d2c",
    textColor: "#FFFFFF",
    imageUrl: "https://bsanderson.storage.googleapis.com/wp-content/uploads/2020/06/12213411/03_dustbringer_placard.jpg",
    catchphrase: "Buscaré el autocontrol",
    herald: "Chanaranach",
    archetype: "El guardián",
    gemstone: "rubí",
    oathTheme:
      " Los juramentos de los Portadores del Polvo giraban en torno a la responsabilidad. Estaban enfocados a comprender que los poderes que empleaban necesitaban ser canalizados de la forma apropiado, así como sus propios deseos y voluntades necesitaban formarse y moldearse adecuadamente. Cuando un Portador del Polvo progresaba en sus juramentos, se les enseñaban grandes poderes de destrucción, y son una de las únicas órdenes cuyas habilidades no estaban disponibles desde el principio, sino que se aprendían poco a poco, conforme pronunciaban los juramentos adecuados. Cada juramento llevaba a una mayor compresión del poder, de la naturaleza de tenerlo, y la responsabilidad asociada.",
    role:
      "Los Portadores del Polvo, aunque a veces se opongan al nombre común de su orden y prefieran ser llamados Liberadores, son contradicciones vivientes entre los Caballeros Radiantes. Creen que un gran poder necesita de una gran fuerza de voluntad para controlarlo. Suelen atraer a los reparadores que gustan de profundizar en el alma y la forma de una cosa, romperla, y ver qué es lo que la hace funcionar. Aún así, sus juramentos están enfocados hacia el control. Han de ser capaces de controlar, contener, y canalizar el terrible poder que guardan en su interior. Tienden a oponerse a quienes se enfocan únicamente en su lado destructivo, ya que argumentan que para crear, uno debe comprender las piezas de la cosa que están intentando hacer. No se ven a sí mismos como algo relacionado con la destrucción, aunque sus poderes son los más destructivo de entre todas las órdenes de Caballeros Radiantes. En cambio, entienden que su naturaleza radica en el control, la precisión y la comprensión. Dentro de los Caballeros Radiantes, solían actuar como el equivalente de la artillería en un ejército moderno. Si querías un amplio sector de tierra destruido o calcinado, llamabas a los Portadores del Polvo. Con todo, a menudo también se les utilizaba como zapadores, ingenieros o estrategas.<br>Atraen a cualquiera que le guste desmontar las cosas, a quien le guste saber cómo funcionan las cosas. También atraen a quienes en ocasiones resultan temerarios, bravos soldados que se ven a sí mismos conteniendo y controlando una terrible destrucción para que no se vaya de las manos y dañe a los inocentes.",
    power1: "División",
    power1Desc: "manipular el ritmo al que algo se descompone",
    power2: "Abrasión",
    power2Desc: "hacer que los objetos, tú incluido, escapen a la fricción",
    blogName: "Portadores del Polvo",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Portadores_del_Polvo"
  },
  {
    name: "Danzantes del Filo",
    color: "#fcf3ee",
    textColor: "#444444",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/04_edgedancer_placard.jpg",
    catchphrase: "Recordaré",
    herald: "Vedeledev",
    archetype: "Curandero",
    gemstone: "diamante",
    oathTheme:
      "Los juramentos de los Danzantes del Filo giran en torno a recordar a las personas comunes del mundo, aquellos que no son poderosos generales ni Radiantes. Con demasiada frecuencia, las acciones de los poderosos tiene terribles efectos sobre las personas sin voz, y los Danzantes del Filo consideran que es su solemne deber recordar que es a las personas a quienes realmente sirven.",
    role:
      "Los Danzantes del Filo son conocidos por ser solícitos y elegantes. Entre los Caballeros Radiantes, ven como su deber el cuidar a la gente y suelen estar menos interesados en la guerra que en intentar mejorar la vida cotidiana de las personas corrientes. A menudo, una ciudad de tamaño medio tendría uno o dos Danzantes del Filo asignados de forma permanente, donde harían uso de la Regeneración para curar y trabajarían por el bien común de la ciudad.<br>Los Danzantes del Filo suelen encontrarse entre los más religiosos de los Radiantes, y son la Orden donde encontrarás con más probabilidad antiguos líderes religiosos que acabaron vinculando un spren. En tiempos de guerra, suelen actuar como médicos móviles, rehuyendo el combate real para curar o poner a resguardo a los heridos, o a quienes han quedado atrapados en terribles situaciones. Aún así, hay algunos que fueron conocidos por su gracia y habilidosa valentía en combate, ocasionalmente utilizados como exploradores o tropas de fuerzas especiales junto a un equipo de Corredores del Viento o Rompedores del Cielo. Uno no debe asumir jamás que los Danzantes del Filo sean vulgares por el simple hecho de ignorar la alta sociedad. Se les conoce como algunos de los Radiantes más elegantes y refinados.",
    power1: "Abrasión",
    power1Desc: "hacer que los objetos, tú incluido, escapen a la fricción",
    power2: "Progresión",
    power2Desc: "sanar organismos y alterar su regeneración.",
    blogName: "Danzantes del Filo",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Danzantes_del_Filo"
  },
  {
    name: "Vigilantes de la Verdad",
    color: "#1e4d39",
    textColor: "#FFFFFF",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/05_truthwatcher_placard.jpg",
    catchphrase: "Buscaré la verdad",
    herald: "Pailiah",
    archetype: "Académico",
    gemstone: "esmeralda",
    oathTheme:
      "Los juramentos de los Vigilantes de la Verdad giran en torno a encontrar la verdad última y compartirla. Están muy preocupados por el conocimiento y la adecuada explotación del mismo. Tened en cuenta que esto no debería ser confundido con los Tejedores de Luz, cuyos juramentos están más ligados a las verdades personales sobre ellos mismo, digamos que por una cuestión de auto-actualización. Los Vigilantes de la Verdad están más preocupados con las verdades fundamentales del universo, y si aquellos con el poder son o no honrados con aquellos a quienes lideran.",
    role:
      "Los Vigilantes de la Verdad son percibidos como tranquilos, largamente conocidos como la Orden de Caballeros Radiantes más erudita. Tienden a atraer principalmente científicos, pero también pensadores eruditos de todo tipo. Esto es extensible a aquellos que normalmente podrían no ser conocidos como eruditos, sino como alguien con frecuencia consumido por sus propios pensamientos. En general, tienden a ser reservados, particularmente en persona, aunque una pequeña minoría de Vigilantes de la Verdad están muy preocupados por las acciones de los poderosos y se les podría comparar con reporteros de investigación. Estos dan a conocer sus opiniones en voz alta y con contundencia, especialmente si creen que alguien en una posición de poder está abusando del mismo, o mintiendo sobre verdades fundamentales. Tened en cuenta que, como pasa con todos los Caballeros Radiantes, hay un gran desencuentro dentro de la Orden sobre qué es la verdad. Aún así, los Vigilantes de la Verdad suelen abordar estas discusiones con entusiasmo, incluso cuando por lo general prefieren escribir sus opiniones más que decirlas en voz alta. Entre los Caballeros Radiantes, los Vigilantes de la Verdad tienden a ser quienes guardan el conocimiento y los secretos de la potenciación, y son quienes descubren la mayoría de los nuevos avances en cosas como la tecnología fabrial.",
    power1: "Progresión",
    power1Desc: "sanar organismos y alterar su regeneración",
    power2: "Iluminación",
    power2Desc: "crear ilusiones",
    blogName: "Vigilantes de la Verdad",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Vigilantes_de_la_Verdad"
  },
  {
    name: "Tejedores de Luz",
    color: "#6c011d",
    textColor: "#FFFFFF",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/06_lightweaver_placard.jpg",
    catchphrase: "Diré mi verdad",
    herald: "Shalash",
    archetype: "Artista",
    gemstone: "granate",
    oathTheme:
      "Los juramentos de los Tejedores de Luz son una rareza, quizás porque su spren tiende a ser el más extraño entre los spren Radiante. En vez de pronunciar palabras específicas, o incluso palabras relacionadas con un tema concreto, los Tejedores de Luz dicen verdades sobre sí mismos, cosas que se admiten a sí mismo a fin de progresar como persona. Se teoriza que debido a que los Tejedores de Luz viven en la frontera entre la realidad y la ficción, es importante para ellos ser capaces de separar lo real de la mentira, y únicamente con la habilidad de hacerlo pueden avanzar.",
    role:
      "Los Tejedores de Luz son los Radiantes más interesados en las artes, incluyendo todo tipo de artes visuales y el teatro. Tienen un espectro muy amplio de personalidades desde el pintor tranquilo e introspectivo hasta el sociable actor de teatro, con todas sus variedades intermedias. Lo que les une suele ser un amor por el arte, aunque hay unos pocos más interesados en la intriga, los secretos y el espionaje. Son los espías de los Caballeros Radiantes, y a menudo los demás desconfían de ellos (como por ejemplo, los estoicos Rompedores del Cielo) por su amor hacia el subterfugio. Poseen la reputación de tener la moral más laxa que otras Órdenes, pero los Tejedores de Luz pronto recalcan que sus valores personales son fuertes. Tan solo es que no sienten la necesidad de coincidir con lo que otras Órdenes más rígidas suelen requerir. Pueden ser menos concisos con sus juramentos, y muchos dicen que hay bastante más de Cultivación en ellos que de Honor (otros ponen en duda este estamento, diciendo que todas las Órdenes tienen una mezcla a partes iguales, a pesar de que algunos spren se llamen honorspren a sí mismos). Los Tejedores de Luz suelen ser espíritus libres, y varios dentro de su Orden ven la importancia del entretenimiento, la belleza y el arte dentro de la vida de una persona, y se esfuerzan para asegurarse de que el mundo no simplemente viva durante las Desolaciones, porque la supervivencia en sí misma no es suficiente, a menos de que haya un motivo por el que vivir.",
    power1: "Iluminación",
    power1Desc: "crear ilusiones",
    power2: "Transformación",
    power2Desc: "moldear objetos de un material en otro",
    blogName: "Tejedores de Luz",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Tejedores_de_Luz"
  },
  {
    name: "Nominadores de lo Otro",
    color: "#125064",
    textColor: "#FFFFFF",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/07_elsecaller_placard.jpg",
    catchphrase: "Alcanzaré mi potencial",
    herald: "Battah",
    archetype: "Consejero",
    gemstone: "circonio",
    oathTheme:
      " Al igual que los juramentos de los Tejedores de Luz y de los Rompedores del Cielo, los juramentos de los Nominadores de lo Otro, están enfocados hacia el individuo. En este caso, el tema es el progreso, mejorar con cada nuevo juramento, persiguiendo explorar su verdadero potencial y alcanzarlo. Es por ello que esta Orden está abierta a muchos tipos diferentes, mientras quieran mejorarse a sí mismos.",
    role:
      "Reflexivos, cuidadosos y cautos, los Nominadores de lo Otro son reconocidos generalmente como los más sabios de los Radiantes. Buscan la mejora personal y una mejora a nivel personal en sus vidas, pero no se encuentran limitados por un tema o conjunto de Ideales específico.  Ello los convierte en una de las órdenes más abiertas y acogedores, aunque tienden a atraer a quienes son menos llamativos. Cuentan con un cierto número de eruditos, pero también atraen a aquellos interesados en el liderazgo. Son buenos animando a los demás, pero algunos son conocidos por poner sus ojos en cosas que quieren, para luego conseguirlas. Dentro de los Caballeros Radiantes suelen estar entre los mejores tácticos, y son genios logísticos, en parte ayudados por sus habilidades para crear comida y agua para los ejércitos, pero también por su habilidad de moverse entrando y saliendo de Shadesmar.",
    power1: "Transformación",
    power1Desc: "moldear objetos de un material en otro",
    power2: "Transportación",
    power2Desc: "viajar entre los reinos Físico y Cognitivo",
    blogName: "Nominadores de lo Otro",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Nominadores_de_lo_Otro"
  },
  {
    name: "Escultores de Voluntad",
    color: "#672861",
    textColor: "#FFFFFF",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/08_willshaper_placard.jpg",
    catchphrase: "Buscaré la libertad",
    herald: "Kalak",
    archetype: "Artesano",
    gemstone: "Amatista",
    oathTheme:
      " Los Escultores de Voluntad creen firmemente que la gente debería ser libre para tomar sus propias decisiones. Sus juramentos están enfocados hacia la libertad y permitir que la gente sea libre para expresarse y seguir su propio camino en la vida.",
    role:
      "Los Escultores de Voluntad tiene reputación de atraer a constructores, artesanos, y creadores a los Radiantes. A pesar de eso, aunque este es un aspecto acertado, los miembros en sí de la Orden son mucho más variopintos. Sus poderes les encaminan hacia la creación cierto, pero sus juramentos están centrados en la libertad y la realización personal. Muchos entre los Escultores de Voluntad son guerreros que buscan liberar a quienes están cautivos, otros están centrados en una expresión personal radical. Los Escultores de Voluntad albergan muchos personajes sociables e incluso alegres que crean su propio camino, tomando la senda que ellos mismos eligen. Les une su amor por construir, pero algunos consideran que la construcción de la sociedad es más importante que la de las estructuras. Entre los Escultores de Voluntad, encontraréis tanto a quienes visten de modo muy conservador, como quienes visten con atuendos más atrevidos y originales. Tiene en común que ambos están de acuerdo en que la libertad para expresar quién eres es una parte importante. Entre los Radiantes, suelen estar enfocados a construir, formar, y crear infraestructuras. Durante la guerra, se les puede enviar a una ciudad para que la fortifiquen contra una invasión en ciernes. Antes o durante el despertar de las Desolaciones, enseñan a la gente cosas sobre saneamiento, trabajos con bronce, y otros temas esenciales. Allí donde encuentres a alguien resistiendo la tiranía o la opresión, a menudo encontrarás a un Escultor de Voluntad animándole.",
    power1: "Transportación",
    power1Desc: "viajar entre los reinos Físico y Cognitivo",
    power2: "Cohesión",
    power2Desc: " alterar la forma de objetos sólidos",
    blogName: "Escultores de Voluntad",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Escultores_de_Voluntad"
  },
  {
    name: "Custodios de Piedra",
    color: "#d26840",
    textColor: "#FFFFFF",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/09_stoneward_placard.jpg",
    catchphrase: "Estaré ahí cuando se me necesite",
    herald: "Talenelat",
    archetype: "Soldier",
    gemstone: "topacio",
    oathTheme:
      "Los juramentos de los Custodios de Piedra se centran en las dinámicas de grupo, en aprender a trabajar con otros, y en estar ahí para quienes les necesiten. Anteponen el interés de los demás al suyo propio, y no retuercen sus Ideales por cuestiones de conveniencia.",
    role:
      "Los Custodios de Piedra son la infantería y las tropas terrestres de los Radiantes, y son conocidos por ser sus mejores soldados (un título que en ocasiones disputan los Corredores del Viento). Suelen atraer a aquellos más interesados en la guerra, el combate con armas, o los deportes de cualquier tipo. Les gustan los retos, y en tiempos de paz se les ve inmersos (y corriendo hacia) varios eventos deportivos tanto de naturaleza militar como de otra naturaleza. Muchos disfrutan estando al aire libre, y encontrarás entre ellos entusiastas de la exploración, así como aquellos que simplemente disfrutan del aire fresco. Suelen ser conocidos por su actitud dinámica y por hacerse cargo de proyectos gigantescos (que a veces son más de lo que pueden manejar). Con todo, muchos están de acuerdo en que el principal atributo de los Custodios de Piedra es su fiabilidad. Aunque en ocasiones sean sociables, jamás son caprichosos. Si un Custodio de Piedra es amigo tuyo, estará allí para ti, y ese es el dogma principal de su Orden: estar allí cuando se les necesita. Otro atributo clave es su  habilidad para afrontar una situación difícil con pocos recursos y hacer algo mejor de ella. Aunque no se les conoce como inventores o creadores, son buenos improvisando soluciones a problemas en el momento.",
    power1: "Cohesión",
    power1Desc: "alterar la forma de objetos sólidos",
    power2: "Tensión",
    power2Desc: "alterar la rigidez de los objetos",
    blogName: "Custodios de Piedra",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Custodios_de_Piedra"
  },
  {
    name: "Forjadores de Vínculos",
    color: "#ebc965",
    textColor: "#444444",
    imageUrl: "https://www.brandonsanderson.com/wp-content/uploads/2020/06/10_bondsmith_placard.jpg",
    catchphrase: "Uniré",
    herald: "Ishi",
    archetype: "Sacerdote",
    gemstone: "Heliodoro",
    oathTheme:
      " Los juramentos de los Forjadores de Vínculos están centrados en la unidad, la unificación, y en unificar a las personas. Con todo, esta es una cuestión un tanto vaga, ya que hay tan pocos Forjadores de Vínculos (y las tres fuentes de sus poderes difieren mucho en cuanto a personalidad) que sus juramentos pueden acabar tomando una variedad de formas, dependiendo de la situación.",
    role:
      "Cualquiera puede convertirse en Forjador de Vínculos, sujeto a persuadir a uno de los tres spren que garantizan los poderes de Forjador de Vínculos. Estos poderes tienden a funcionar de forma distinta de un Forjador de Vínculos a otro, e incluso las potencias que comparten con otras Órdenes suelen funcionar de un modo distinto para los Forjadores de Vínculos.<br>Los Forjadores de Vínculos son poco frecuentes, en el sentido de que nunca hay más de tres miembros completos. Históricamente, trabajaron para resolver disputas y ayudar a organizar gobiernos funcionales. Aunque únicamente puedan haber tres miembros completos, han habido épocas en las que algunos Forjadores de Vínculos tomaron escuderos. Además, muchos entre el séquito que protegían a los Forjadores de Vínculos fueron considerados miembros de la Orden, llegando incluso a pronunciar sus juramentos, aunque nunca tuvieron un spren ni llegarían a tenerlo. Algunas personas dijeron que esta es la forma más pura de ser un radiante, porque fueron juramentos pronunciados no en nombre de ganar unos poderes, sino simplemente, por decir los propios juramentos en sí.<br>Generalmente, los Forjadores de Vínculos  son el corazón y alma de los radiantes, los más protegidos y tenidos en alta consideración por las Órdenes, capaces de hacer cosas increíbles con la naturaleza de sus juramentos, vínculos, y poder. La Orden, incluyendo los ya mencionados escuderos y asistentes, tendían a atraer a los pacificadores del mundo, a quienes quieren unir a la gente, en vez de dividirla.",
    power1: "Tensión",
    power1Desc: "alterar la rigidez de los objetos",
    power2: "Adhesión",
    power2Desc: "unir cosas",
    blogName: "Forjadores de Vínculos",
    blogLink: "https://es.coppermind.net/wiki/Orden_de_los_Forjadores_de_V%C3%ADnculos"
  }
];

var traitData = {
  "1b": [35,	75,	20,	15,	80,	0,	100,	35,	50,	70],
  "2b": [25,	0,	10,	60,	100,	30,	20,	25,	15,	30],
  "3b": [60,	40,	100,	20,	15,	85,	0,	65,	75,	80],
  "4b": [24,	45,	42,	83,	88,	45,	10,	10,	35,	49],
  "5b": [90,	55,	95,	47,	10,	50,	13,	57,	93,	30],
  "6b": [10,	0,	61,	25,	89,	55,	100,	45,	23,	20],
  "7b": [9,	52,	100,	7,	47,	53,	41,	59,	65,	0],
  "8b": [45,	79,	52,	10,	85,	41,	80,	53,	37,	0],
  "9b": [15,	25,	70,	35,	100,	43,	20,	11,	42,	0],
  "10b": [0,	15,	80,	10,	50,	90,	30,	70,	15,	20],
  "11b": [10,	100,	55,	0,	20,	25,	79,	42,	50,	25],
  "12b": [35,	90,	15,	0,	100,	10,	85,	20,	40,	15],
  "13b": [48,	60,	12,	61,	100,	39,	85,	0,	50,	75],
  "14b": [60,	0,	23,	85,	45,	81,	75,	100,	30,	70],
  "15b": [45,	75,	87,	50,	50,	13,	79,	15,	85,	70],
  "16b": [25,	15,	0,	8,	45,	85,	57,	100,	15,	11],
  "17b": [69,	88,	45,	20,	53,	0,	25,	30,	100,	20],
  "18b": [12,	15,	100,	15,	50,	78,	13,	60,	0,	10],
  "19b": [70,	75,	45,	0,	100,	85,	10,	90,	10,	30],
  "20b": [35,	100,	65,	50,	60,	20,	15,	25,	0,	20],
  "21b": [25,	11,	55,	69,	22,	31,	44,	75,	30,	70],
  "23b": [0,	25,	22,	55,	85,	100,	15,	75,	15,	15],
  "24b": [75,	85,	23,	59,	85,	25,	22,	15,	30,	90],
  "25b": [25,	15,	85,	20,	20,	75,	0,	70,	20,	20],
  "26b": [85,	85,	47,	90,	49,	35,	0,	30,	70,	100],
  "27b": [55,	81,	45,	60,	89,	31,	85,	30,	47,	80],
  "28b": [15,	55,	55,	0,	15,	100,	76,	53,	45,	10],
  "29b": [75,	90,	0,	40,	85,	25,	88,	100,	70,	25],
  "30b": [65,	31,	40,	0,	40,	45,	15,	85,	100,	20],
  "31b": [25,	45,	100,	0,	41,	35,	10, 75,	76,	25],
  "32b": [42,	75,	40,	22,	80,	0,	100,	64,	80,	15],
  "33b": [78,	70,	80,	50,	0,	60,	50,	50,	100,	75],
  "34b": [0,	10,	100,	10,	41,	69,	79,	85,	50,	20],
  "35b": [58,	20,	20,	100,	84,	59,	16,	25,	0,	70],
  "36b": [25,	40,	20,	10,	0,	70,	30,	20,	70,	0],
  "37b": [40,	38,	60,	20,	20,	35,	0,	100,	40,	10]
};

var quizPrompts = [
  {
    promptLeftText: "Como un libro abierto",
    promptRightText: "Cara de poker",
    traitLeft: "1a",
    traitRight: "1b"
  },
  {
    promptLeftText: "Seguro de tí mismo",
    promptRightText: "Necesitas aprobación",
    traitLeft: "2a",
    traitRight: "2b"
  },
  {
    promptLeftText: "Precavido",
    promptRightText: "Atrevido",
    traitLeft: "3a",
    traitRight: "3b"
  },
  {
    promptLeftText: "Biblioteca",
    promptRightText: "Cuadrilátero",
    traitLeft: "5a",
    traitRight: "5b"
  },
  {
    promptLeftText: "Parte de la manada",
    promptRightText: "Lobo solitario",
    traitLeft: "6a",
    traitRight: "6b"
  },
  {
    promptLeftText: "Pacificador",
    promptRightText: "Incendiario",
    traitLeft: "7a",
    traitRight: "7b"
  },
  {
    promptLeftText: "Espiritual",
    promptRightText: "Escéptico",
    traitLeft: "8a",
    traitRight: "8b"
  },
  {
    promptLeftText: "Líder",
    promptRightText: "Moderador",
    traitLeft: "9a",
    traitRight: "9b"
  },
  {
    promptLeftText: "Perro guardián",
    promptRightText: "Gato callejero",
    traitLeft: "10a",
    traitRight: "10b"
  },
  {
    promptLeftText: "Compasivo",
    promptRightText: "Indiferente",
    traitLeft: "11a",
    traitRight: "11b"
  },
  {
    promptLeftText: "Corazón",
    promptRightText: "Cabeza",
    traitLeft: "12a",
    traitRight: "12b"
  },
  {
    promptLeftText: "Extravagante",
    promptRightText: "Reservado",
    traitLeft: "13a",
    traitRight: "13b"
  },
  {
    promptLeftText: "Ley al pie de la letra",
    promptRightText: "Interpretas la ley",
    traitLeft: "14a",
    traitRight: "14b"
  },
  {
    promptLeftText: "Espíritu libre",
    promptRightText: "Disciplinado",
    traitLeft: "15a",
    traitRight: "15b"
  },
  {
    promptLeftText: "Obediente",
    promptRightText: "Rebelde",
    traitLeft: "16a",
    traitRight: "16b"
  },
  {
    promptLeftText: "Creativo",
    promptRightText: "Conservador",
    traitLeft: "17a",
    traitRight: "17b"
  },
  {
    promptLeftText: "Fiable",
    promptRightText: "Flexible",
    traitLeft: "18a",
    traitRight: "18b"
  },
  {
    promptLeftText: "Con los pies en la tierra",
    promptRightText: "Estar en las nubes",
    traitLeft: "19a",
    traitRight: "19b"
  },
  {
    promptLeftText: "Pensamiento innovador",
    promptRightText: "Seguir las normas",
    traitLeft: "20a",
    traitRight: "20b"
  },
  {
    promptLeftText: "Tenso",
    promptRightText: "Relajado",
    traitLeft: "21a",
    traitRight: "21b"
  },
  {
    promptLeftText: "Decidido",
    promptRightText: "Indeciso",
    traitLeft: "23a",
    traitRight: "23b"
  },
  {
    promptLeftText: "Te gustan los cambios",
    promptRightText: "Te gusta la estabilidad",
    traitLeft: "24a",
    traitRight: "24b"
  },
  {
    promptLeftText: "Planificador",
    promptRightText: "Espontáneo",
    traitLeft: "25a",
    traitRight: "25b"
  },
  {
    promptLeftText: "El fin justifica los medios",
    promptRightText: "Acciones honorables",
    traitLeft: "26a",
    traitRight: "26b"
  },
  {
    promptLeftText: "Jovial",
    promptRightText: "Serio",
    traitLeft: "27a",
    traitRight: "27b"
  },
  {
    promptLeftText: "Decir la verdad",
    promptRightText: "Retorcer la verdad",
    traitLeft: "28a",
    traitRight: "28b"
  },
  {
    promptLeftText: "Te gusta desmontar cosas",
    promptRightText: "Si no está roto, no lo toques",
    traitLeft: "29a",
    traitRight: "29b"
  },
  {
    promptLeftText: "Hotel",
    promptRightText: "Camping",
    traitLeft: "30a",
    traitRight: "30b"
  },
  {
    promptLeftText: "Esgrima",
    promptRightText: "Boxeo",
    traitLeft: "31a",
    traitRight: "31b"
  },
  {
    promptLeftText: "Más de arte",
    promptRightText: "Más de ciencias",
    traitLeft: "32a",
    traitRight: "32b"
  },
  {
    promptLeftText: "Sabiduría académica",
    promptRightText: "Universidad de la vida",
    traitLeft: "33a",
    traitRight: "33b"
  },
  {
    promptLeftText: "Paladin",
    promptRightText: "Pícaro",
    traitLeft: "34a",
    traitRight: "34b"
  },
  {
    promptLeftText: "Competitivo",
    promptRightText: "Informal",
    traitLeft: "35a",
    traitRight: "35b"
  },
  {
    promptLeftText: "Sin secretos",
    promptRightText: "Comparte lo imprescindible",
    traitLeft: "36a",
    traitRight: "36b"
  }
];

// For each prompt, create a list item to be inserted in the list group
function createPromptItems() {
  for (var i = 0; i < quizPrompts.length; i++) {
    var prompt_li = document.createElement("li");

    prompt_li.setAttribute("class", "list-group-item rounded-lg prompt");
    var leftTextSpan = document.createElement("span");
    leftTextSpan.className = "left";
    var leftText = document.createTextNode(quizPrompts[i].promptLeftText + "\u00A0\u00A0");
    leftTextSpan.appendChild(leftText);
    prompt_li.appendChild(leftTextSpan);
    var leftPctSpan = document.createElement("span");
    leftPctSpan.className = "left pct font-weight-bold";
    leftPctSpan.innerHTML = "50%";
    prompt_li.appendChild(leftPctSpan);

    var rightTextSpan = document.createElement("span");
    rightTextSpan.className = "right";
    var rightText = document.createTextNode("\u00A0\u00A0" + quizPrompts[i].promptRightText);
    rightTextSpan.appendChild(rightText);
    prompt_li.appendChild(rightTextSpan);
    var rightPctSpan = document.createElement("span");
    rightPctSpan.className = "right pct font-weight-bold";
    rightPctSpan.innerHTML = "50%";
    prompt_li.appendChild(rightPctSpan);

    var clearDiv = document.createElement("div");
    clearDiv.className = "floatClear";
    prompt_li.appendChild(clearDiv);

    var group = document.createElement("div");
    group.className = "column slider-group slider-group-justified";

    var slider = document.createElement("input");
    slider.setAttribute("type", "range");
    slider.setAttribute("min", 0);
    slider.setAttribute("max", 100);
    slider.setAttribute("value", 50);
    slider.className = "slider custom-range";
    var inputHandler = updateSliderValue.bind(prompt_li);
    slider.oninput = inputHandler;
    group.appendChild(slider);

    prompt_li.appendChild(group);

    document.getElementById("quiz").appendChild(prompt_li);
  }
}

function updateSliderValue() {
  var newValue = this.getElementsByClassName("slider")[0].value
  var color = Math.floor(Math.abs(50-newValue) * 5).toString(16);
  var leftPctSpan = this.getElementsByClassName("left pct")[0];
  leftPctSpan.innerHTML = (100 - newValue) + "%";
  var rightPctSpan = this.getElementsByClassName("right pct")[0];
  rightPctSpan.innerHTML = newValue + "%";
  if (newValue > 50) {
    leftPctSpan.setAttribute("style", "color:#" + color + "0000");
    rightPctSpan.setAttribute("style", "color:#00" + color + "00");
  } else if (newValue < 50) {
    leftPctSpan.setAttribute("style", "color:#00" + color + "00");
    rightPctSpan.setAttribute("style", "color:#" + color + "0000");
  }
  jQuery(function ($) {
  $("#submit-btn").prop('disabled', false);
  });
}

createPromptItems();

function sortWithIndices(toSort) {
  for (var i = 0; i < toSort.length; i++) {
    toSort[i] = [toSort[i], i];
  }
  toSort.sort(function(left, right) {
    return left[0] < right[0] ? -1 : 1;
  });
  toSort.sortIndices = [];
  for (var j = 0; j < toSort.length; j++) {
    toSort.sortIndices.push(toSort[j][1]);
    toSort[j] = toSort[j][0];
  }
  return toSort;
}

function normalizeResults(results) {
  var normalizedResults = [];
  for (var i = 0; i < results.length; i++) {
    normalizedResults[i] = Math.floor((120000 - results[i]) / 1200);
  }
  return normalizedResults;
}

function calculateResults() {
  var results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  var sliders = document.getElementsByClassName("slider");
  var promptTrait;
  for (var i = 0; i < quizPrompts.length; i++) {
    var promptSliderValue = sliders[i].value;
    promptTrait = quizPrompts[i].traitRight;
    var tempResults = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    for (var j = 0; j < orders.length; j++) {
      tempResults[j] = Math.abs(traitData[promptTrait][j] - promptSliderValue) ** 2;
      results[j] += tempResults[j];
    }
    console.log("Trait " + promptTrait + " resulted in " + tempResults);
  }
  results[9] *= 1.3;
  console.log("Order totals: " + results);
  return results;
}

jQuery(function ($) {
  $("#submit-btn").click(function () {
  var results = calculateResults();
  console.log(results)
  var chosenOrder = 0;
  var lowScore = 999999;
  for (var k = 0; k < results.length; k++) {
    if (results[k] < lowScore) {
      console.log('chosen order:'+ k)
      chosenOrder = k;
      lowScore = results[k];
    }
  }
  var results = sortWithIndices(results);
  var normalizedResults = normalizeResults(results);

  // After clicking submit, add up the totals from answers
  // For each group, find the value that is active
  $(".results").removeClass("d-none");
  $(".results").addClass("d-block");


    var progressBars = document.createElement("div");
  progressBars.id = "progressBars";
  progressBars.className = "container";
  for (var i = 0; i < results.length; i++) {
    progressBars.innerHTML += `
<div class="row align-items-center pg-row">
  <div class="order-titles">
	<div class="p-1 col-12 text-center pg-text">${orders[results.sortIndices[i]]}</div>
  </div>
</div>
<div class="row align-items-center pg-row">
  <div class="progress col-11 pg-back" style="height: 30px">
    <div class="progress-bar pg-front" style="height: 30px; width:${normalizedResults[i]}%; background-color:${orderData[results.sortIndices[i]].color} !important; color:${orderData[results.sortIndices[i]].textColor} !important"></div>
  </div>
  <div class="col-1 pg-percent" style="height: 30px; color:black !important">
	<div class="text-center">
		${normalizedResults[i]}%
	</div>
  </div>
</div>`;
  }

/*  var progressBars = document.createElement("div");
  progressBars.id = "progressBars";
  progressBars.className = "container d-flex";
  for (var i = 0; i < results.length; i++) {
    progressBars.innerHTML += `
<div class="d-flex flex-column align-items-right">
  <div class="d-flex flex-row text-right">${orders[results.sortIndices[i]]}</div>`;
  }
  for (i = 0; i< results.length; i++) {
    progressBars.innerHTML += `
    <div class="d-flex flex-row">
<div class="progress col-8" style="height: 25px">
    <div class="progress-bar" style="height: 25px; width:${normalizedResults[i]}%; background-color:${orderData[results.sortIndices[i]].color} !important; color:${orderData[results.sortIndices[i]].textColor} !important">${normalizedResults[i]}%</div>
  </div>
</div>
    </div>`;
  }
  progressBars.innerHTML += `</div>`;*/

  document.getElementById("results").innerHTML = `
<div class='text-left'>
Pronuncia otra vez los antiguos juramentos: Vida antes que muerte. Fuerza antes que debilidad. Viaje antes que destino.<p>
<img src="${orderData[chosenOrder].imageUrl}" class="img-fluid"><p>
<h2>${orderData[chosenOrder].name} - ${orderData[chosenOrder].catchphrase}</h2>
Perteneces a la orden de los ${orderData[chosenOrder].name} la cual da acceso a las Potencias de ${orderData[chosenOrder].power1} y ${orderData[chosenOrder].power2}. La ${orderData[chosenOrder].power1} te permite ${orderData[chosenOrder].power1Desc}. La ${orderData[chosenOrder].power2} te permite ${orderData[chosenOrder].power2Desc}.<p>
${orderData[chosenOrder].oathTheme}<p>
${orderData[chosenOrder].role}<p>
Lee más sobre los ${orderData[chosenOrder].name} <a href="${orderData[chosenOrder].blogLink}">aquí</a>.<p>
Si esta Orden no te encaja o no es lo que estabas esperando, lee más sobre cada Orden <a href="https://cosmere.es/a-que-orden-de-caballeros-radiantes-perteneces-e-informacion-actualizada-sobre-los-mismos/">aquí</a> y elije tu favorita<p> Aquí tienes un detalle de cómo te alineas con cada Orden:
` + progressBars.outerHTML + `
<P> <P>

</div>
  `;

  // Hide the quiz after they submit their results
  $("#quiz-container").addClass("d-none");
  $("#submit-btn").addClass("d-none");
  $("#retake-btn").removeClass("d-none");
  $("#edit-btn").removeClass("d-none");
  window.scrollTo(0, 0);
});

  });

function resetSliderValues() {
  var sliders = document.getElementsByClassName("slider");
  for (var i = 0; i < sliders.length; i++) {
    sliders[i].value = 50;
  }
  var pcts = document.getElementsByClassName("pct");
  for (var j = 0; j < pcts.length; j++) {
    pcts[j].innerHTML = "50%";
    pcts[j].setAttribute("style", "color:black");
  }
}

function setUIToQuiz() {
	jQuery(function ($) {
	$('#quiz-container').removeClass('d-none');
	});
	jQuery(function ($) {
	$('#submit-btn').removeClass('d-none');
	});
	jQuery(function ($) {
	$('#retake-btn').addClass('d-none');
	});
	jQuery(function ($) {
	$('#edit-btn').addClass('d-none');
	});
	jQuery(function ($) {
	$('.results').addClass('d-none');
	});
	jQuery(function ($) {
	$('.results').removeClass('d-block');
	});
  window.scrollTo(0, 0);
}


// Refresh the screen to show a new quiz if they click the retake quiz button
jQuery(function ($) {
	$("#retake-btn").click(function () {
  resetSliderValues();
	setUIToQuiz();
});
});

jQuery(function ($) {
$("#edit-btn").click(function () {
  setUIToQuiz();
});
});