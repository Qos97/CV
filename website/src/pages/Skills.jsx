import {
  Server, Package, HardDrive, Cloud, Settings, Lock,
  BarChart3, Building2, ShieldCheck, ClipboardList, Bot,
} from 'lucide-react'
import { useLang } from '../LanguageContext'
import content from '../content.json'
import './Skills.css'

const SKILL_ICONS = {
  server: Server,
  package: Package,
  storage: HardDrive,
  cloud: Cloud,
  automation: Settings,
  network: Lock,
  monitoring: BarChart3,
  infra: Building2,
  compliance: ShieldCheck,
  practices: ClipboardList,
  ai: Bot,
}

export default function Skills() {
  const { lang } = useLang()
  const t = content[lang].skills

  return (
    <section className="section section--alt skills-page">
      <div className="container">
        <p className="section-label">{t.label}</p>
        <h1 className="section-title">{t.title}</h1>

        <div className="skills-grid">
          {t.groups.map(g => {
            const Icon = SKILL_ICONS[g.icon]
            return (
            <div key={g.category} className="skill-card">
              <div className="skill-card__header">
                <Icon className="skill-card__icon" size={20} aria-hidden="true" />
                <h3 className="skill-card__title">{g.category}</h3>
              </div>
              <div className="skill-card__tags">
                {g.items.map(item => (
                  <span key={item} className="tag">{item}</span>
                ))}
              </div>
            </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
