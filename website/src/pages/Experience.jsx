import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Experience.css'

export default function Experience() {
  const { lang } = useLang()
  const t = content[lang].experience

  return (
    <section className="section exp-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>

        <div className="timeline">
          {t.jobs.map((job, i) => (
            <div key={i} className={`timeline__item${job.status === 'current' ? ' timeline__item--current' : ''}`}>
              <div className="timeline__marker">
                <div className="timeline__dot" />
                {i < t.jobs.length - 1 && <div className="timeline__line" />}
              </div>

              <div className="timeline__content">
                <div className="timeline__header">
                  <div>
                    <h2 className="timeline__company">{job.company}</h2>
                    <h3 className="timeline__role">{job.role}</h3>
                    <span className="timeline__meta">{job.period} · {job.location}</span>
                  </div>
                  {job.status === 'current' && (
                    <span className="badge badge--green">{t.current}</span>
                  )}
                </div>

                <p className="timeline__desc">{job.description}</p>

                <ul className="timeline__bullets">
                  {job.bullets.map((b, bi) => <li key={bi}>{b}</li>)}
                </ul>

                <div className="timeline__tags">
                  {job.tags.map(tag => <span key={tag} className="tag">{tag}</span>)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
