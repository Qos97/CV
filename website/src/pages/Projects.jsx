import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Projects.css'

export default function Projects() {
  const { lang } = useLang()
  const t = content[lang].projects

  return (
    <section className="section projects-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>
        <p className="projects-intro">{t.intro}</p>

        <div className="projects-grid">
          {t.list.map((p, i) => (
            <div key={i} className="project-card">
              <div className="project-card__header">
                <h2 className="project-card__title">{p.title}</h2>
                <span className={`badge badge--${p.statusType}`}>{p.status}</span>
              </div>
              <p className="project-card__desc">{p.description}</p>
              <ul className="project-card__bullets">
                {p.bullets.map((b, bi) => <li key={bi}>{b}</li>)}
              </ul>
              <div className="project-card__tags">
                {p.tags.map(tag => <span key={tag} className="tag">{tag}</span>)}
              </div>
            </div>
          ))}
        </div>

        <div className="projects-note">
          <span>💡</span>
          <span>{t.note}</span>
        </div>
      </div>
    </section>
  )
}
