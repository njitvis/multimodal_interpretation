const Analysis = ({ children, goal, obs, next }) => {
	return (
		<div className="grid grid-cols-[4fr_1fr] min-h-screen gap-4 p-4">
			<div className="p-6 bg-gray-100 rounded-2xl shadow-md flex items-center justify-center">
				{children}
			</div>

			<div className="p-6 bg-white rounded-2xl shadow-md overflow-y-auto max-h-screen">
				<h2 className="text-xl font-semibold">{goal}</h2>
				<h4 className="font-semibold">Observation</h4>
				<ul key="parent" className="list-disc pl-5 space-y-3 ">
					{
						obs.map((ob) => {
							if (typeof ob === typeof {}) {
								return (Object.keys(ob).map(item => (
									<>
										<li key={item} className="font-semibold">{item}</li>
										<ul key={`child=${item}`} className="list-disc pl-5">
											{
												ob[item].map((o) => (
													<li key={o}>{o}</li>
												))
											}
										</ul>
									</>
								)))
							} else {
								return (
									<li key={ob}>{ob}</li>
								)
							}
						})
					}
				</ul>
				<h4 className="font-semibold">Next Steps</h4>
				<ul className="list-disc pl-5 space-y-3 ">
					{
						next && next.map((n) => (
							<li key={n}>{n}</li>
						))
					}
				</ul>
			</div>
		</div>
	);
};

export default Analysis;