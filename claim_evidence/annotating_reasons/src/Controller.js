const Controller = ({setCurrentIndex, nextPage, savePage}) => {
	return (
		<div className="p-4 border-t flex justify-between">
        <button
          onClick={() => setCurrentIndex(i => Math.max(i - 1, 0))}
          className="px-4 py-2 bg-gray-300 rounded"
        >
          Previous Page
        </button>
        <div className="flex gap-2">
          <button
            onClick={nextPage}
            className="px-4 py-2 bg-gray-300 rounded"
          >
            Next Page
          </button>
          <button
            onClick={savePage}
            className="px-4 py-2 bg-green-600 text-white rounded"
          >
            Save
          </button>
        </div>
      </div>
	);
}

export default Controller;