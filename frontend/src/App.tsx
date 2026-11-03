import { useEffect, useState } from "react";

type Health = { status: string };

export default function App() {
  const [language, setLanguage] = useState<"en" | "ru" | "kk">("en");
  const [apiStatus, setApiStatus] = useState("Checking connection…");
  const [confirming, setConfirming] = useState(false);
  const [demoNotice, setDemoNotice] = useState("");

  useEffect(() => {
    fetch("/api/health")
      .then((response) => {
        if (!response.ok) throw new Error("API unavailable");
        return response.json() as Promise<Health>;
      })
      .then((data) => setApiStatus(data.status === "ok" ? "Connected" : "Unavailable"))
      .catch(() => setApiStatus("Backend unavailable"));
  }, []);

  const copy = {
    en: { title: "Your safety matters", subtitle: "A simple way to prepare and reach trusted people.", sos: "SOS", start: "Activate SOS", cancel: "Cancel", confirm: "Confirm emergency alert?", note: "Demo interface only. No message is sent to contacts or emergency services.", contacts: "Trusted contacts", safe: "Safe Walk", status: "System status" },
    ru: { title: "Ваша безопасность важна", subtitle: "Простой способ подготовиться и связаться с близкими.", sos: "SOS", start: "Активировать SOS", cancel: "Отмена", confirm: "Подтвердить сигнал тревоги?", note: "Демонстрационный интерфейс. Сообщения контактам и экстренным службам не отправляются.", contacts: "Доверенные контакты", safe: "Безопасная прогулка", status: "Состояние системы" },
    kk: { title: "Сіздің қауіпсіздігіңіз маңызды", subtitle: "Жақын адамдарыңызбен байланысуға дайын болыңыз.", sos: "SOS", start: "SOS іске қосу", cancel: "Болдырмау", confirm: "Дабыл сигналын растайсыз ба?", note: "Бұл тек демонстрациялық интерфейс. Ешкімге хабарлама жіберілмейді.", contacts: "Сенімді контактілер", safe: "Қауіпсіз серуен", status: "Жүйе күйі" }
  }[language];

  function activateDemo() {
    setConfirming(false);
    setDemoNotice("Demo only: SOS flow is not connected to real notification services yet.");
  }

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Qalqan home"><span className="brand-mark">Q</span> qalqan</a>
        <label className="language">
          <span className="sr-only">Language</span>
          <select value={language} onChange={(event) => setLanguage(event.target.value as "en" | "ru" | "kk")} aria-label="Language">
            <option value="en">English</option><option value="ru">Русский</option><option value="kk">Қазақша</option>
          </select>
        </label>
      </header>

      <section className="hero">
        <div className="eyebrow"><span className="pulse" /> PERSONAL SAFETY COMPANION</div>
        <h1>{copy.title}</h1>
        <p className="subtitle">{copy.subtitle}</p>
        <div className="sos-wrap">
          <button className="sos-button" onClick={() => { setConfirming(true); setDemoNotice(""); }} aria-label={copy.start}>
            <span>{copy.sos}</span><small>{copy.start}</small>
          </button>
        </div>
        {confirming && <div className="confirm-panel" role="dialog" aria-label={copy.confirm}>
          <strong>{copy.confirm}</strong>
          <div className="actions"><button className="button primary" onClick={activateDemo}>Confirm (demo)</button><button className="button" onClick={() => setConfirming(false)}>{copy.cancel}</button></div>
        </div>}
        {demoNotice && <p className="notice" role="status">{demoNotice}</p>}
        <p className="safety-note">{copy.note}</p>
      </section>

      <section className="feature-grid" aria-label="Safety features">
        <article className="feature-card"><span className="feature-icon">♡</span><h2>{copy.contacts}</h2><p>Plan who you would contact in an emergency.</p><span className="tag">Coming next</span></article>
        <article className="feature-card"><span className="feature-icon">⌖</span><h2>Location sharing</h2><p>Location sharing will require your permission.</p><span className="tag">Coming next</span></article>
        <article className="feature-card"><span className="feature-icon">◷</span><h2>{copy.safe}</h2><p>A timer and manual check-ins for a planned walk.</p><span className="tag">Coming next</span></article>
      </section>

      <footer className="footer"><span>Qalqan · Kazakhstan</span><span>{copy.status}: <b>{apiStatus}</b></span></footer>
    </main>
  );
}