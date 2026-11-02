import Reveal from '../components/ui/Reveal';

const steps = [
  {
    number: '01',
    label: 'RICONOSCERE',
    title: 'Ci sono vittime?',
    text: 'Un primo modello valuta se l’evento è senza morti.',
  },
  {
    number: '02',
    label: 'STIMARE',
    title: 'Se sì, quante?',
    text: 'Un secondo modello stima il numero, imparando dai casi noti.',
  },
  {
    number: '03',
    label: 'CONTROLLARE',
    title: 'I conti tornano?',
    text: 'Rispettiamo i fatti certi e arrotondiamo senza perdere il totale stimato.',
  },
];

export default function ModelArchitecture() {
  return (
    <section className="model-architecture wrap" aria-labelledby="model-architecture-title">
      <Reveal className="model-architecture-intro">
        <span className="eyebrow">DENTRO IL MODELLO · LIGHTGBM</span>
        <h2 id="model-architecture-title">
          Prima capire.
          <br />
          <span>Poi contare.</span>
        </h2>
        <p>
          Due modelli si dividono il compito.
          <br />
          Un controllo finale protegge i numeri.
        </p>
      </Reveal>
      <div className="model-architecture-steps">
        {steps.map((step, index) => (
          <Reveal key={step.number} delay={index * 0.05}>
            <article className="model-architecture-step">
              <div className="model-architecture-step-label">
                <span>{step.number}</span>
                {step.label}
              </div>
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </article>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
