import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Contact.css'

export default function Contact() {
  const { lang } = useLang()
  const t = content[lang].contact

  return (
    <section className="section contact-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>

        <div className="contact__layout">
          <div className="contact__intro">
            <p>{t.intro1}</p>
            <p>{t.intro2}</p>
          </div>

          <div className="contact__cards">
            <a href="https://linkedin.com/in/fgfernandes97" target="_blank" rel="noreferrer" className="contact-card">
              <div className="contact-card__icon contact-card__icon--blue">in</div>
              <div>
                <div className="contact-card__label">LinkedIn</div>
                <div className="contact-card__value">linkedin.com/in/fgfernandes97</div>
                <div className="contact-card__action">{t.linkedinAction}</div>
              </div>
            </a>

            <div className="contact-card contact-card--static">
              <div className="contact-card__icon">📍</div>
              <div>
                <div className="contact-card__label">{t.locationLabel}</div>
                <div className="contact-card__value">{t.locationValue}</div>
                {t.locationAction && <div className="contact-card__action">{t.locationAction}</div>}
              </div>
            </div>

            <div className="contact-card contact-card--static">
              <div className="contact-card__icon">📄</div>
              <div>
                <div className="contact-card__label">{t.cvLabel}</div>
                <div className="contact__cv-links">
                  <a href="/CV_Filipe_Fernandes_EN.pdf" download className="btn btn-primary">{t.cvEN}</a>
                  <a href="/CV_Filipe_Fernandes_PT.pdf" download className="btn btn-outline">{t.cvPT}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
