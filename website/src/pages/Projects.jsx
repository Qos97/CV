import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Projects.css'

function ProjectGrid({ list }) {
  return (
    <div className="projects-grid">
      {list.map((p, i) => (
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
  )
}

export default function Projects() {
  const { lang } = useLang()
  const t = content[lang].projects

  return (
    <section className="section projects-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>
        <p className="projects-intro">{t.intro}</p>

        <h2 className="projects-group-title">{t.workTitle}</h2>
        <ProjectGrid list={t.workList} />

        <h2 className="projects-group-title">{t.personalTitle}</h2>
        <ProjectGrid list={t.personalList} />

        <div className="projects-note">
          <span>💡</span>
          <span>{t.note}</span>
        </div>
      </div>
    </section>
  )
}
