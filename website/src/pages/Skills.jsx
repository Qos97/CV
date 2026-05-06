import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Skills.css'

export default function Skills() {
  const { lang } = useLang()
  const t = content[lang].skills

  return (
    <section className="section section--alt skills-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>

        <div className="skills-grid">
          {t.groups.map(g => (
            <div key={g.category} className="skill-card">
              <div className="skill-card__header">
                <span className="skill-card__icon">{g.icon}</span>
                <h3 className="skill-card__title">{g.category}</h3>
              </div>
              <div className="skill-card__tags">
                {g.items.map(item => (
                  <span key={item} className="tag">{item}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
