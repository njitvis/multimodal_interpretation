import { X } from 'lucide-react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';


const ClaimEvidenceSection = ({ currentPage, addClaim, updateClaim, deleteClaim, updateClaimOrder, updateEvidence, addEvidence, deleteEvidence }) => {
	const reorder = (list, startIndex, endIndex) => {
		const result = Array.from(list);
		const [removed] = result.splice(startIndex, 1);
		result.splice(endIndex, 0, removed);
		return result;
	};

	const onDragEnd = (result) => {
		if (!result.destination) return;
		const newClaims = reorder(
			currentPage.claims,
			result.source.index,
			result.destination.index
		);
		updateClaimOrder(newClaims);
	};



	return (
		<div id='claims-section' className="flex-1 p-6 overflow-y-auto">

			<DragDropContext onDragEnd={onDragEnd}>
				<Droppable droppableId="claimsSection">
					{(provided) => (
						<div
							id="claims-section"
							className="flex-1 p-6 overflow-y-auto"
							ref={provided.innerRef}
							{...provided.droppableProps}
						>
							{currentPage.claims.map((c, idx) => (
								<Draggable key={idx} draggableId={`claim-${idx}`} index={idx}>
									{(prov, snapshot) => (
										<div
											ref={prov.innerRef}
											{...prov.draggableProps}
											{...prov.dragHandleProps}
											className={`mb-6 p-4 border rounded-lg ${snapshot.isDragging ? 'bg-gray-100' : ''
												}`}
										>
											<div key={idx} className="mb-6 p-4 border rounded-lg">
												<div className='flex justify-between align-top gap-5'>
													<div className='flex-grow'>
														<label className="block mb-1 font-semibold">Claim {idx + 1}</label>
														<input
															type="text"
															value={c.claim}
															onChange={e => updateClaim(idx, 'claim', e.target.value)}
															className="w-full mb-3 p-1 border rounded"
														/>
													</div>
													<button
														onClick={() => deleteClaim(idx)}
														className="text-gray-500 hover:text-red-500"
													>
														<X size={16} />
													</button>
												</div>

												<label className="block mb-1 font-semibold">Reasoning Strategy</label>
												<input
													type="text"
													value={c.strategy}
													onChange={e => updateClaim(idx, 'strategy', e.target.value)}
													className="w-full mb-3 p-1 border rounded"
												/>

												<label className="block mb-1 font-semibold">List of Evidence</label>
												{c.evidences.map((ev, j) => (
													<div key={j} className="flex items-center mb-2 gap-2">
														<input
															type="text"
															placeholder="Evidence"
															value={ev}
															onChange={e => updateEvidence(idx, j, e.target.value)}
															className="flex-1 p-1 border rounded mr-2"
														/>
														<select
															value={ev}
															onChange={e => {
																if (e.target.value !== "") {
																	updateEvidence(idx, j, e.target.value)
																}
															}}
															className="p-1 border rounded"
														>
															<option value="">From chart + caption + context</option>
															{currentPage.claims.map((c, k) => (
																<option key={k} value={c.claim}>
																	Claim {k + 1}
																</option>
															))}
														</select>
														<button
															onClick={() => deleteEvidence(idx, j)}
															className="text-gray-500 hover:text-red-500"
														>
															<X size={16} />
														</button>
													</div>
												))}
												<button
													onClick={() => addEvidence(idx)}
													className="mt-2 px-3 py-1 bg-gray-200 rounded"
												>
													Add Evidence
												</button>
											</div>
										</div>
									)}
								</Draggable>
							))}
							{provided.placeholder}
						</div>
					)}
				</Droppable>
			</DragDropContext>


			<button
				onClick={addClaim}
				className="mb-4 px-4 py-2 bg-blue-500 text-white rounded"
			>
				Add Claim Section
			</button>
		</div>
	);
}


export default ClaimEvidenceSection;