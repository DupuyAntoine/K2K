import PropTypes from 'prop-types'
import { useEffect, useState } from "react"
import { fetchDomains } from "../api/api"

export default function DomainSelector ({ domain, setDomain }) {
  const [domains, setDomains] = useState([])

  useEffect(() => {
    fetchDomains().then(setDomains)
  }, [])

  return (
    <div className="flex gap-2 items-center">
      <label htmlFor="domain" className="text-sm font-semibold">Domain:</label>
      <select
        id="domain"
        disabled={domains.length === 0}
        className="border border-gray-300 rounded px-2 py-1"
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
      >
        <option value="">-- Select a domain --</option>
        {domains.map((d) => (
          <option key={d.id} value={d.id}>{d.label}</option>
        ))}
      </select>
    </div>
  )
}

DomainSelector.propTypes = {
  domain: PropTypes.string.isRequired,
  setDomain: PropTypes.func.isRequired,
}
