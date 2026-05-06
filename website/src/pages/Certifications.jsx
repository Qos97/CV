import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Certifications.css'

export default function Certifications() {
  const { lang } = useLang()
  const t = content[lang].certifications

  return (
    <section className="section section--alt certs-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>

        <div className="certs-note">
          <span>ℹ️</span>
          <span>{t.note}</span>
        </div>

        <h2 className="certs-subtitle">{t.subtitle}</h2>

        <div className="certs-grid">
          {t.list.map((c, i) => (
            <div key={i} className="cert-card">
              <div className="cert-card__header">
                <div>
                  <div className="cert-card__acronym">{c.name}</div>
                  <div className="cert-card__full">{c.full}</div>
                  <div className="cert-card__vendor">{c.vendor}</div>
                </div>
                <span className={`badge badge--${c.statusType}`}>{c.status}</span>
              </div>
              <p className="cert-card__why">{c.why}</p>
              <div className="cert-card__tags">
                {c.tags.map(tag => <span key={tag} className="tag">{tag}</span>)}
              </div>
            </div>
          ))}
        </div>

        <h2 className="certs-subtitle certs-subtitle--training">{t.trainingSubtitle}</h2>

        <div className="training-list">
          {t.training.map((tr, i) => (
            <div key={i} className="training-item">
              <div className="training-item__meta">
                <span className="training-item__date">{tr.date}</span>
                <span className="training-item__hours">{tr.hours}</span>
              </div>
              <div className="training-item__body">
                <div className="training-item__name">{tr.name}</div>
                <div className="training-item__platform">
                  {tr.platform}
                  {tr.verifyUrl && (
                    <a href={tr.verifyUrl} target="_blank" rel="noreferrer" className="training-item__verify">
                      Verify ↗
                    </a>
                  )}
                </div>
                <div className="training-item__tags">
                  {tr.tags.map(tag => <span key={tag} className="tag">{tag}</span>)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
