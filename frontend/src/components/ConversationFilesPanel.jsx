import PropTypes from "prop-types"

export default function ConversationFilesPanel({ files }) {
  if (!files || files.length === 0) return null
  console.log(files)
  return (
    <div className="w-72 p-4 border-l bg-white shadow">
      <h2 className="text-md font-semibold mb-2">Associated Files</h2>
      <ul className="space-y-2 text-sm max-h-[80vh] overflow-y-auto">
        {files.map((file, index) => (
          <li key={index} className="break-all">
            <a
              href={file.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              {file.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  )
}

ConversationFilesPanel.propTypes = {
  files: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string,
      url: PropTypes.string,
      description: PropTypes.string,
    })
  ),
}
