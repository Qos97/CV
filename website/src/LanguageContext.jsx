import { createContext, useContext, useState } from 'react'

const LanguageContext = createContext()

function getSavedLang() {
  try {
    const saved = localStorage.getItem('lang')
    if (saved === 'en' || saved === 'pt') return saved
  } catch {}
  return 'en'
}

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(getSavedLang)

  function setLang(l) {
    try { localStorage.setItem('lang', l) } catch {}
    setLangState(l)
  }

  return (
    <LanguageContext.Provider value={{ lang, setLang }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLang() {
  return useContext(LanguageContext)
}
