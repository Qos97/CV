import { Link } from 'react-router-dom'
import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Home.css'

const TECH = [
  'Kubernetes', 'Ceph', 'Docker', 'VMware vSphere',
  'Fortinet FortiGate', 'WatchGuard', 'HAProxy',
  'Zabbix', 'Prometheus', 'Grafana',
  'Microsoft 365', 'Azure AD', 'PowerShell', 'Ansible',
]

export default function Home() {
  const { lang } = useLang()
  const t = content[lang].home

  return (
    <div className="home">
      <section className="hero">
        <div className="container hero__content">
          <div className="hero__badge">
            <span className="hero__dot" /> {t.badge}
          </div>
          <h1 className="hero__name">Filipe Fernandes</h1>
          <p className="hero__title">{t.title}</p>
          <p className="hero__sub">{t.sub}</p>
          <p className="hero__location">{t.location}</p>
          <div className="hero__actions">
            <Link to="/experience" className="btn btn-primary">{t.viewExp}</Link>
            <a
              href={lang === 'en' ? '/CV_Filipe_Fernandes_EN.pdf' : '/CV_Filipe_Fernandes_PT.pdf'}
              download
              className="btn btn-outline"
            >{t.downloadCV}</a>
          </div>
        </div>
      </section>

      <section className="section section--alt highlights">
        <div className="container">
          <div className="highlights__grid">
            {t.highlights.map(h => (
              <div key={h.label} className="highlight-card">
                <span className="highlight-card__icon">{h.icon}</span>
                <strong className="highlight-card__label">{h.label}</strong>
                <span className="highlight-card__sub">{h.sub}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section tech-strip">
        <div className="container">
          <p className="section-label" style={{ textAlign: 'center', marginBottom: 24 }}>
            {t.techLabel}
          </p>
          <div className="tech-strip__tags">
            {TECH.map(tech => <span key={tech} className="tag">{tech}</span>)}
          </div>
        </div>
      </section>

      <section className="section section--alt cta-block">
        <div className="container cta-block__inner">
          <div>
            <h2 className="cta-block__title">{t.ctaTitle}</h2>
            <p className="cta-block__sub">{t.ctaSub}</p>
          </div>
          <div className="cta-block__actions">
            <Link to="/about" className="btn btn-primary">{t.ctaAbout}</Link>
            <Link to="/contact" className="btn btn-outline">{t.ctaContact}</Link>
          </div>
        </div>
      </section>
    </div>
  )
}
