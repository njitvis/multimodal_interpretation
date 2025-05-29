const Source = ({currentPage, updateCurrentPage, loadFromFile}) => {
	return (
		<div className="w-1/3 p-4 border-r flex flex-col overflow-y-auto">
          <label className="mb-2 font-semibold">Load JSON</label>
          <input type="file" accept=".json" onChange={loadFromFile} className="mb-4" />

          <label className="mb-1 font-semibold">Chart Image URL</label>
          <input
            type="text"
            value={currentPage.chartSrc}
            onChange={e => updateCurrentPage({ chartSrc: e.target.value })}
            className="mb-2 p-1 border rounded"
          />
          {currentPage.chartSrc && (
            <img
              src={currentPage.chartSrc}
              alt="Chart"
              className="mb-4 max-h-48 object-contain"
            />
          )}

          <label className="mb-1 font-semibold">Caption</label>
          <textarea
            rows={10}
            value={currentPage.caption}
            onChange={e => updateCurrentPage({ caption: e.target.value })}
            className="mb-4 p-1 border rounded resize-none"
          />

          <label className="mb-1 font-semibold">Context</label>
          <textarea
            rows={15}
            value={currentPage.context}
            onChange={e => updateCurrentPage({ context: e.target.value })}
            className="mb-4 p-1 border rounded resize-none"
          />
        </div>
	);
}


export default Source;