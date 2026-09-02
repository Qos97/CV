import { MapPin, Globe, GraduationCap, Download } from 'lucide-react'
import LinkedinIcon from '../components/LinkedinIcon'
import { useLang } from '../LanguageContext'
import content from '../content.json'
import './About.css'

export default function About() {
  const { lang } = useLang()
  const t = content[lang].about

  return (
    <section className="section about-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>

        <div className="about__grid">
          <div className="about__text">
            {t.paragraphs.map((p, i) => (
              <p key={i} dangerouslySetInnerHTML={{ __html: p }} />
            ))}

            <div className="about__meta">
              <div className="about__meta-item">
                <MapPin className="about__meta-icon" size={16} role="img" aria-label="Location" />
                <span>Barreiro, Setúbal, Portugal</span>
              </div>
              <div className="about__meta-item">
                <Globe className="about__meta-icon" size={16} role="img" aria-label="Languages" />
                <span>{t.metaLang}</span>
              </div>
              <div className="about__meta-item">
                <GraduationCap className="about__meta-icon" size={16} role="img" aria-label="Education" />
                <span>{t.metaEdu}</span>
              </div>
            </div>
          </div>

          <div className="about__sidebar">
            <div className="about__stats">
              {t.stats.map(s => (
                <div key={s.label} className="stat-card">
                  <span className="stat-card__value">{s.value}</span>
                  <span className="stat-card__label">{s.label}</span>
                </div>
              ))}
            </div>

            <div className="about__contact-card">
              <h3>{t.contactTitle}</h3>
              <a href="https://linkedin.com/in/fgfernandes97" target="_blank" rel="noreferrer" className="about__contact-link">
                <LinkedinIcon size={16} /> linkedin.com/in/fgfernandes97
              </a>
              <a href="/CV_Filipe_Fernandes_EN.pdf" download className="btn btn-primary" style={{ marginTop: 16, justifyContent: 'center' }}>
                <Download size={16} aria-hidden="true" /> {t.downloadEN}
              </a>
              <a href="/CV_Filipe_Fernandes_PT.pdf" download className="btn btn-outline" style={{ marginTop: 8, justifyContent: 'center' }}>
                <Download size={16} aria-hidden="true" /> {t.downloadPT}
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
