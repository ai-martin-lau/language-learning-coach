[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

# Language Learning Coach

Un Skill adaptativo para Codex que convierte el aprendizaje de idiomas en una práctica continua: input fiable, expresiones útiles, producción activa, interacción real, feedback específico y repaso diferido.

La lección cambia según el idioma, la variedad, la modalidad, el objetivo y el desempeño observado del estudiante. Puede trabajar con lenguas habladas y escritas, lenguas de signos, lenguas clásicas, lenguas construidas y lenguas con pocos recursos cuando existen materiales fiables.

> [!IMPORTANT]
> Este es un proyecto independiente de código abierto inspirado en las prácticas de aprendizaje que Kazuma ha compartido públicamente. No es oficial ni está autorizado, afiliado o respaldado por Kazuma.

## Qué lo hace diferente

Muchas sesiones de idiomas con IA terminan como conversaciones aisladas. Language Learning Coach está diseñado como un curso continuo:

- **Tareas reales antes que progreso abstracto:** los objetivos se convierten en acciones observables, como pedir una comida o responder preguntas de seguimiento.
- **Expresiones útiles y después uso flexible:** se aprenden expresiones completas con contexto, patrones de respuesta y elementos sustituibles, no como guiones rígidos.
- **Práctica antes que explicación:** el coach empieza con input e interacción y después explica un patrón gramatical de alto valor a partir de lo que acabas de usar.
- **Evidencia en lugar de rachas:** el dominio depende de la recuperación sin ayuda, la transferencia, la interacción y el desempeño diferido, no del tiempo invertido ni del número de tarjetas repasadas.
- **Adaptación específica al idioma:** los tonos, los sistemas de escritura, la morfología compleja, el registro, el espacio de signación y las tradiciones históricas cambian el diseño de la lección.
- **Estado local persistente:** el perfil, el banco de expresiones, la evidencia de desempeño y la próxima cola de repasos pueden mantenerse como archivos Markdown legibles.

## Funciones principales

- Incorporación inicial que empieza con una única pregunta exacta: **`你要学习什么语言？`** («¿Qué idioma quieres aprender?»)
- Lecciones diarias adaptativas, mantenimiento de cinco minutos, estudio profundo y revisión de experiencias reales.
- Práctica de comprensión oral y pronunciación con audio fiable y límites honestos sobre las herramientas.
- Adaptación basada en vídeo para lenguas de signos, incluidos los componentes manuales y no manuales.
- Gramática práctica, vocabulario activo, conversación, lectura, escritura y preparación específica para exámenes.
- Comprobaciones diferidas de recuperación y transferencia con seis estados de evidencia, desde `new` hasta `retained`.
- Una lengua activa y, de forma predeterminada, una rotación de mantenimiento para las lenguas adicionales.
- Exportación opcional a Anki basada en recuperar una expresión a partir de una situación, no en pares de palabras aisladas.
- Verificación de fuentes y tratamiento explícito con `needs_confirmation` para lenguas con pocos recursos o sensibles para su comunidad.

## Requisitos e instalación

Necesitas Codex con compatibilidad para Skills locales. Git es necesario para el método manual y Python 3 para el método que utiliza el instalador incluido.

### Instalar con el instalador de Skills incluido

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ai-martin-lau/language-learning-coach \
  --path . \
  --name language-learning-coach
```

### Instalar con Git

```bash
git clone https://github.com/ai-martin-lau/language-learning-coach.git \
  ~/.codex/skills/language-learning-coach
```

También puedes descargar el repositorio y copiar su contenido a:

```text
~/.codex/skills/language-learning-coach
```

Después de instalarlo, inicia una nueva tarea de Codex para que se detecte el Skill.

## Inicio rápido

Invoca directamente el Skill:

```text
Usa $language-learning-coach para ayudarme a aprender un idioma.
```

Si no has indicado un idioma, su primera respuesta solo contiene:

```text
你要学习什么语言？
```

También puedes empezar con un objetivo concreto:

```text
Usa $language-learning-coach. Empiezo japonés desde cero y tengo 15 minutos
al día. Quiero mantener conversaciones básicas durante un viaje a Japón.
```

```text
Usa $language-learning-coach. Ayúdame a presentarme en un evento de la comunidad
de lengua de signos americana. Puedo ver y grabar vídeos cortos.
```

```text
Usa $language-learning-coach. Continúa la lección de portugués de Brasil de ayer.
Hoy solo tengo cinco minutos.
```

El coach solo pide la información que cambia la siguiente lección y después empieza una pequeña tarea real, en lugar de devolver un cuestionario largo o un plan de estudio genérico.

## Cómo se adaptan las lecciones

| Característica del idioma o del objetivo | Adaptación |
|---|---|
| Tono, acento tonal, duración o contrastes de acento | Contrastes perceptivos antes de la producción, seguidos de práctica a nivel de oración |
| Un sistema de escritura nuevo o complejo | El sonido y la escritura progresan juntos; la transliteración recibe un plan de retirada gradual |
| Flexión rica o aglutinación | Expresiones completas junto con análisis temprano de raíces y afijos y producción controlada |
| Registro, honoríficos, continuos dialectales o diglosia | Cada expresión se vincula a la relación, la región y el medio |
| Lenguas de signos | El vídeo fiable, el espacio de signación, el movimiento, la orientación y los marcadores no manuales sustituyen el trabajo de pronunciación |
| Lenguas clásicas, históricas o litúrgicas | Se priorizan la tradición textual, la morfología, la evidencia de corpus y una tradición de pronunciación identificada |
| Lenguas con pocos recursos o sensibles para su comunidad | Se prefieren fuentes comunitarias o institucionales y no se inventa contenido incierto |
| Objetivos de examen, lectura, escritura, trabajo, viaje o lengua de herencia | El equilibrio entre destrezas y la tarea de evaluación cambian para adaptarse al objetivo real |

No existe una lista fija de «idiomas compatibles». La compatibilidad depende de la modalidad solicitada y de la calidad de las fuentes disponibles, y el coach debe indicar cuándo no puede verificar algo.

## Estado de aprendizaje y privacidad

Cuando el espacio de trabajo actual permite escritura, el coach puede mantener:

```text
language-learning/<language-slug>/
├── profile.md
├── phrase-bank.md
└── progress.md
```

Estos archivos solo guardan información pertinente para el curso: objetivos y restricciones, expresiones contextualizadas y sus fuentes, desempeño observado, correcciones y repasos programados. Permanecen en el espacio de trabajo del usuario y nunca se escriben en el directorio donde está instalado el Skill.

El repositorio no contiene telemetría, integración de cuentas ni servicios en segundo plano. Codex y las herramientas que autorice el usuario aún pueden acceder a fuentes externas cuando una lección requiera material lingüístico actual o fiable; siguen aplicándose las normas de privacidad propias de esos productos y herramientas.

## Método y evidencia

El ciclo operativo es:

```text
input fiable → expresión en contexto → percepción e imitación → generación
→ interacción → feedback específico → recuperación diferida
```

El diseño se inspira en las explicaciones públicas de Kazuma sobre la imitación del sonido desde el inicio, las expresiones útiles, el vocabulario activo, la gramática práctica, los hábitos constantes basados en tareas y la inmersión guiada por intereses. Consulta [el resumen del método y las fuentes primarias](references/kazuma-method.md).

Estas prácticas no se presentan como un sistema completo validado científicamente. El Skill contrasta cada decisión con investigaciones sobre adquisición de segundas lenguas relacionadas con la enseñanza de la pronunciación, las secuencias formulaicas, la gramática explícita, la interacción y el feedback correctivo, el espaciamiento y la recuperación, el input centrado en el significado y la autorregulación. Consulta [la matriz de evidencia y las salvaguardas](references/evidence-and-guardrails.md).

El coach **no** promete fluidez en un número fijo de días, un acento nativo, idéntica calidad de recursos para todos los idiomas ni dominio basado únicamente en rachas, tiempo invertido, aciertos en el mismo día o precisión en Anki.

## Estructura del repositorio

```text
.
├── SKILL.md                         # Instrucciones principales de comportamiento y enrutamiento
├── agents/openai.yaml              # Metadatos de presentación en Codex
├── assets/learning-workspace/      # Plantillas para la continuidad del curso
├── references/
│   ├── kazuma-method.md             # Fuentes públicas del método y sus límites
│   ├── evidence-and-guardrails.md   # Investigación sobre adquisición de segundas lenguas y límites científicos
│   ├── language-adaptation.md       # Adaptación según características lingüísticas
│   └── session-protocols.md         # Lecciones, feedback, repaso y estado
└── docs/plans/                      # Registros de diseño
```

## Contribuciones

Se agradecen issues y pull requests, especialmente para:

- correcciones respaldadas por fuentes primarias o reconocidas por la comunidad;
- una mejor adaptación para tipos de lengua u objetivos de aprendizaje con poca representación;
- límites más claros sobre seguridad, cultura, accesibilidad y evidencia;
- mejoras naturales de cualquiera de las cinco traducciones del README.

Usa el `README.md` en inglés como fuente de contenido y actualiza todas las traducciones afectadas en el mismo pull request. No añadas promesas de fluidez sin respaldo, consenso inventado entre hablantes nativos ni afirmaciones de afiliación con Kazuma.

## Licencia

Publicado bajo la [Licencia MIT](LICENSE).
