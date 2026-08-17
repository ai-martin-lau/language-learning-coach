[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

# Language Learning Coach

**Empieza con una tarea de viaje real y construye una base verificable de nivel A2 por la ruta práctica más corta que permita tu desempeño.**

![Un viaje ilustrado por una estación de tren, un hotel y un restaurante](assets/readme/travel-hero.webp)

Language Learning Coach es una Skill adaptativa de Codex para aprender idiomas modernos que cuentan con recursos fiables y abundantes, mediante tareas reales, expresiones útiles, recuperación activa, interacción, correcciones específicas y reevaluaciones posteriores.

Está pensada ante todo para aprender idiomas con fines de viaje, como el francés, el alemán, el italiano, el español, el portugués, el coreano, el japonés, el árabe y el inglés. El idioma, la variedad regional, el sistema de escritura, el tiempo disponible y lo que realmente seas capaz de hacer determinan cómo será la lección.

> [!IMPORTANT]
> «A2 para viajar» es la ruta de aprendizaje de este proyecto, no un subnivel oficial del CEFR ni un certificado. A2 abarca intercambios sencillos y directos en situaciones conocidas y rutinarias; el CEFR sitúa en B1 la capacidad de afrontar la mayoría de las situaciones que pueden surgir durante un viaje. Por eso, el objetivo del coach es que puedas **desenvolverte con más seguridad en tareas de viaje habituales y previsibles**, no prometer que podrás afrontar sin dificultad cualquier viaje o emergencia. Consulta la [escala global](https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale) y los [descriptores de expresión oral](https://www.coe.int/en/web/common-european-framework-reference-languages/table-3-cefr-3.3-common-reference-levels-qualitative-aspects-of-spoken-language-use) del Consejo de Europa.

> [!NOTE]
> Este es un proyecto independiente de código abierto inspirado en las prácticas de aprendizaje que Kazuma ha compartido públicamente. No es un proyecto oficial de Kazuma, no está afiliado a él ni cuenta con su autorización o respaldo.

## Empezar rápido no significa aprender por atajos

El coach acorta la distancia entre «quiero aprender» y comprar un billete, registrarte en un hotel, pedir comida, preguntar cómo llegar o reparar una conversación. La primera lección elige una tarea probable del próximo viaje, enseña únicamente entre una y tres expresiones completas necesarias para resolverla y te pide que las uses de inmediato.

No se omiten las fuentes fiables, la práctica con condiciones distintas ni las reevaluaciones posteriores. «Rápido» significa eliminar listas de vocabulario, secuencias gramaticales, calendarios genéricos y materiales ajenos al próximo viaje; no prometer un A2 instantáneo, un plazo fijo ni criterios menos exigentes.

## Aprende para el viaje, no para mantener una racha

![Seis áreas centrales de práctica para viajar: transporte, alojamiento, comida, orientación, compras y reparación de la comunicación](assets/readme/travel-scenarios.svg)

La ruta de viaje predeterminada sigue siete resultados. La imagen muestra seis ámbitos cotidianos de interacción; el séptimo es una petición de ayuda básica con límites de seguridad:

- **Transporte:** preguntar por billetes, andenes, horarios, trayectos y cambios.
- **Alojamiento:** hacer el registro de entrada, confirmar datos y explicar un problema sencillo.
- **Comida:** pedir, expresar preferencias, entender una pregunta habitual y pagar.
- **Orientación:** preguntar cómo llegar, identificar puntos de referencia y confirmar que has entendido.
- **Compras:** preguntar por precios, cantidades, tallas y disponibilidad, y efectuar el pago.
- **Reparación de la comunicación:** pedir que repitan, hablen más despacio, lo escriban, lo señalen o lo expresen de otra manera.
- **Ayuda básica:** resolver una consulta en una farmacia, objetos perdidos u otra petición no urgente sin tratar emergencias graves como tareas A2.

Cada expresión activa se guarda con tu propia versión, un elemento sustituible, una pregunta de seguimiento probable y una fórmula para reparar la comunicación. El objetivo no es memorizar un libro de frases rígido, sino completar la tarea cuando cambia un dato.

Las emergencias médicas, legales, migratorias o de seguridad graves no se presentan como situaciones que el nivel A2 permita afrontar de forma autónoma y segura.

## Empieza con una sola frase

```text
Usa $language-learning-coach. Empiezo japonés desde cero, tengo 15 minutos
al día y quiero mantener conversaciones básicas durante un viaje a Japón.
```

Si todavía no has indicado un idioma, la primera respuesta contiene únicamente:

```text
¿Qué idioma quieres aprender?
```

A partir de ahí, el coach hace una sola pregunta cada vez, y únicamente cuando la respuesta vaya a cambiar la siguiente lección. Empiezas con una tarea pequeña en lugar de recibir un cuestionario largo o un calendario genérico.

También puedes empezar así:

```text
Usa $language-learning-coach. Ayúdame a formular peticiones corteses en árabe egipcio.
Distingue la variedad oral local del árabe estándar moderno.
```

```text
Usa $language-learning-coach. Continúa la lección de portugués de Brasil de ayer.
Hoy solo tengo cinco minutos.
```

## La ruta útil más corta se adapta a ti

![Un ciclo de ocho etapas que va de una tarea real de viaje a material fiable, recuperación, interacción, correcciones y transferencia diferida](assets/readme/adaptive-loop.svg)

Si tu objetivo de viaje incluye comprensión y expresión oral, una lección típica recorre estos pasos:

1. elegir una tarea real y la variedad lingüística objetivo;
2. escuchar un modelo completo y clasificado antes de ver la respuesta;
3. comprender la intención y un dato fundamental;
4. aprender entre una y tres expresiones completas con elementos sustituibles;
5. recuperarlas y transformarlas a medida que desaparecen las ayudas;
6. completar una interacción breve con una pregunta de seguimiento y una opción para reparar la comunicación;
7. corregir uno o dos problemas que afecten directamente al éxito de la tarea y repetirla inmediatamente;
8. volver a intentarlo más adelante tras cambiar el lugar, la hora, la persona, el objeto o la condición.

El orden cambia para objetivos exclusivamente de lectura o escritura, necesidades de accesibilidad, sistemas de escritura nuevos, contrastes de tono o acento tonal, flexión compleja, honoríficos, variedades regionales o situaciones de diglosia. Viajar es la ruta principal; los objetivos de trabajo, exámenes, lectura, escritura, contenidos audiovisuales y lengua de herencia siguen estando disponibles cuando existen recursos fiables.

## Una microlección, cuatro pasos visibles

![Una lección en cuatro viñetas: escuchar un modelo completo, intentar la tarea, recibir una corrección específica y repetir con una condición distinta](assets/readme/lesson-storyboard.svg)

1. **Modelo:** escucha la expresión completa de una fuente clasificada; el texto aparece después cuando corresponde.
2. **Intento:** úsala en una tarea de taquilla, recepción de hotel, restaurante, tienda u orientación.
3. **Corrección específica:** mantén vivo el intercambio y corrige solo lo que más afecte a la tarea.
4. **Nuevo intento:** completa la tarea otra vez y cambia después una condición para que el resultado dependa de la recuperación, no de copiar.

El juego de rol con IA es una simulación útil. No demuestra que hayas sido capaz de desenvolverte con un hablante nativo, a velocidad natural, con ruido de fondo, ante un acento nuevo o frente a una respuesta imprevisible del mundo real.

## Rumbo a A2, con evidencia separada por destreza

![Seis destrezas lingüísticas que avanzan hacia práctica con apoyo, realización independiente, transferencia a condiciones distintas y retención diferida](assets/readme/evidence-ladder.svg)

La comprensión oral, la producción oral, la lectura, la escritura, la interacción y la pronunciación se registran por separado. Entender una expresión al oírla no cuenta automáticamente como saber decirla; leer en voz alta no demuestra que puedas interactuar; acertar durante la misma sesión no demuestra retención.

La escala de evidencia es:

```text
con apoyo → realización independiente → cambio de condición → retención diferida
```

El espacio de trabajo registra la tarea, el nivel de ayuda, el entorno de la evidencia, el **medio de respuesta**, el resultado, la fecha y la próxima reevaluación. Así, una romanización escrita, un «ya lo dije» que el coach no pudo observar o una tarea aún pendiente de respuesta no se guardan por error como habla audible o escritura en el sistema normal del idioma. Una misión de viaje solo avanza a logro en la misma sesión, cambio de condición, retención diferida o comprobación real cuando existe evidencia compatible.

Completar una misión no equivale a alcanzar A2. La evaluación interna de tipo A2 solo se supera cuando al menos cinco de los siete ámbitos de viaje definidos alcanzan una comprobación diferida o real con expresiones centrales distintas, se incluye la reparación de la comunicación, las seis capacidades tienen evidencia retenida vinculada a requisitos exactos de misión y al menos una misión se supera con una persona o tarea real. Incluso entonces, el coach solo puede decir que la evidencia concuerda con un desempeño de tipo A2 **en las tareas evaluadas** y señalar todas las carencias. Esto no es un resultado del CEFR; solo una evaluación externa adecuada puede establecerlo. La velocidad de avance depende del idioma, el punto de partida, el tiempo de práctica, la calidad de los recursos y de que el desempeño resista la transferencia y el paso del tiempo.

## Las fuentes de audio nunca se ocultan

Para objetivos orales, cuando hay audio reproducible, se escucha la frase nueva antes de ver su forma escrita. Cada modelo se clasifica así:

| Clase de fuente | Qué significa | Qué puede respaldar |
|---|---|---|
| `native_official` | Grabación oficial o institucional realizada por un hablante nativo de la variedad objetivo | Un modelo sólido para el material exacto que cubre la fuente |
| `native_traceable` | Grabación de un hablante nativo cuya procedencia puede verificarse y cuya variedad, contexto y registro son adecuados | Un modelo dentro del alcance documentado de la fuente |
| `tts` | Voz sintética de respaldo, siempre identificada como tal | Comprensión inicial y ensayo; no acredita un modelo nativo ni el dominio de la pronunciación |
| `pending` | Todavía no se ha proporcionado un modelo fiable | El paso oral o de pronunciación se detiene en vez de inventarse |

Cuando se usa TTS, el espacio de trabajo registra por separado la comprobación de la expresión y el registro, la variedad objetivo, el motor o la voz, el archivo o reproductor entregado y la validación técnica. Que una onda de audio se reproduzca no demuestra que la formulación sea natural.

Los archivos WAV locales se validan estructuralmente antes de entregarse. La validez técnica nunca sustituye la fiabilidad de la fuente, la variedad correcta, la reproducción efectiva ni una evaluación de la pronunciación.

## Instalación

Necesitas Codex con compatibilidad para Skills locales y Python 3 para los validadores incluidos de audio y del espacio de trabajo. El validador de audio acepta archivos WAV RIFF PCM clásicos sin comprimir; convierte antes cualquier otro formato. La instalación con Git también requiere Git.

### Instalador de Skills incluido

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ai-martin-lau/language-learning-coach \
  --path . \
  --name language-learning-coach
```

### Git

```bash
git clone https://github.com/ai-martin-lau/language-learning-coach.git \
  ~/.codex/skills/language-learning-coach
```

También puedes descargar el repositorio y copiar su contenido a:

```text
~/.codex/skills/language-learning-coach
```

Después de la instalación, abre una nueva tarea de Codex para que se detecte la Skill.

## Cómo cambia la ruta según el idioma

| Característica del idioma o del objetivo | Adaptación |
|---|---|
| Contrastes de tono, acento tonal, duración o acento prosódico | Contrastes perceptivos antes de producir, seguidos de práctica con frases completas |
| Un sistema de escritura nuevo o complejo | El sonido y la escritura avanzan juntos; la transliteración sigue un plan de retirada gradual |
| Flexión abundante o aglutinación | Expresiones completas junto con análisis temprano de raíces y afijos y producción controlada |
| Registro, honoríficos, continuos dialectales o diglosia | Cada expresión conserva la relación, la región y el medio en que se usa |
| Objetivos de lectura, escritura, trabajo, examen, contenidos audiovisuales o lengua de herencia | El equilibrio de destrezas y las tareas de evidencia cambian para ajustarse al objetivo real |

Los ejemplos no constituyen una lista permanente de idiomas compatibles. Otro idioma moderno, hablado o escrito, entra dentro del alcance cuando dispone de audio fiable, diccionarios, referencias gramaticales y evidencia de uso. Las lenguas de signos, clásicas, construidas o con pocos recursos requieren materiales especializados o acompañamiento fuera del alcance actual de esta Skill.

## Estado de aprendizaje local y privacidad

Cuando el espacio de trabajo actual permite escritura, el coach puede mantener:

```text
language-learning/<language-slug>/
├── profile.md
├── phrase-bank.md
├── function-map.md
└── progress.md       # misiones de viaje, reevaluaciones y evidencia de clase
```

Estos archivos Markdown legibles guardan objetivos y restricciones pertinentes para el curso, anclas de hábito, expresiones contextualizadas, clases de fuente de audio, evidencia por destreza, cobertura de funciones iniciales, correcciones y reevaluaciones programadas. Permanecen en el espacio de trabajo del usuario, no en el directorio donde está instalada la Skill. Un validador incluido comprueba la estructura y la coherencia interna sin afirmar que el resultado de aprendizaje registrado sea verdadero.

El repositorio no contiene telemetría, integración de cuentas ni servicios en segundo plano. Codex y las herramientas autorizadas por el usuario pueden acceder a fuentes externas cuando una lección necesite material lingüístico fiable; siguen aplicándose las políticas de privacidad de esos productos.

## Método y evidencia

El diseño se inspira en las explicaciones públicas de Kazuma sobre imitar primero el sonido, aprender expresiones útiles, activar el vocabulario, estudiar gramática práctica, mantener hábitos constantes basados en tareas y usar material vinculado a los propios intereses. Consulta [el resumen del método y las fuentes primarias](references/kazuma-method.md).

Estas prácticas no se tratan como un único sistema validado científicamente. La Skill contrasta cada decisión con investigaciones sobre adquisición de segundas lenguas relacionadas con la enseñanza de la pronunciación, las secuencias formulaicas, la gramática explícita, la interacción y la corrección, el espaciamiento y la recuperación, el input orientado al significado y la autorregulación. Consulta [la matriz de evidencia y las salvaguardas](references/evidence-and-guardrails.md).

La navegación visual de este README toma como referencia la sección de aprendizaje de idiomas de [byoungd/up](https://github.com/byoungd/up). Todo el texto y las imágenes de este repositorio son originales; no se han reutilizado fotos ni ilustraciones del proyecto de referencia.

## Estructura del repositorio

```text
.
├── SKILL.md                         # Instrucciones principales de comportamiento y enrutamiento
├── agents/openai.yaml              # Metadatos de presentación en Codex
├── assets/
│   ├── learning-workspace/          # Plantillas para la continuidad del curso
│   └── readme/                      # Recursos visuales originales del README
├── references/
│   ├── kazuma-method.md             # Fuentes públicas del método y sus límites
│   ├── evidence-and-guardrails.md   # Investigación sobre adquisición de segundas lenguas y límites científicos
│   ├── language-adaptation.md       # Adaptación según las características lingüísticas
│   └── session-protocols.md         # Lecciones, correcciones, repaso y estado
├── scripts/validate_audio.py        # Validador de archivos WAV PCM locales
├── scripts/validate_workspace.py    # Validador del estado de aprendizaje en Markdown
├── tests/test_validate_audio.py     # Pruebas de regresión del validador de audio
├── tests/test_validate_workspace.py # Pruebas de regresión del validador del espacio de trabajo
└── docs/plans/                      # Registros de diseño
```

## Contribuciones

Los issues y pull requests son bienvenidos, en especial las correcciones respaldadas por fuentes, una mejor adaptación a las principales variedades lingüísticas y tareas de viaje, límites más claros de seguridad y evidencia, y mejoras naturales en las cinco traducciones del README.

Usa el `README.md` en inglés como fuente de contenido y actualiza en el mismo pull request todas las traducciones afectadas. No añadas afirmaciones de alcanzar A2 en un plazo fijo, promesas de fluidez sin respaldo, consensos inventados entre hablantes nativos, testimonios falsos ni afirmaciones de afiliación con Kazuma.

## Licencia

Publicado bajo la [Licencia MIT](LICENSE).
