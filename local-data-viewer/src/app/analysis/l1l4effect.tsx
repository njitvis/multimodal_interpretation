"use client";

import { useEffect, useState } from "react";
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import Analysis from "./Analysis";
import { CaptionInfo, CaptionInfoRead } from "@/types";
import * as d3 from "d3";
import Heatmap from "./heatmap";
import HorizontalBar from "./horizontalBar";
import { Input } from "@/components/ui/input";

const L1l4Effect = () => {
	const [captionInfo, setCaptionInfo] = useState<CaptionInfo[]>([]);
	const [sortKey, setSortKey] = useState<keyof CaptionInfo>("interpretability_rating");
	const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
	const [filterMin, setFilterMin] = useState<number | null>(null);
	const [filterMax, setFilterMax] = useState<number | null>(null);

	useEffect(() => {
		const loadData = async () => {
			const readCaptionInfo: CaptionInfo[] = [];
			await d3.csv("/data/download.csv", (data: CaptionInfoRead) => {
				const vector = data.l1_l4_vector
					.substring(1, data.l1_l4_vector.length - 1)
					.split(', ').map(vector => parseInt(vector));

				const minVal = Math.min(...vector);
				const maxVal = Math.max(...vector);

				// Apply MinMax Scaling: (x - min) / (max - min)
				const scaledVector = vector.map(v => (maxVal !== minVal ? (v - minVal) / (maxVal - minVal) : 0));

				const caption: CaptionInfo = {
					chart_type: data.chart_type,
					clarity: data.clarity,
					complexity: data.complexity,
					imageid: data.image_id,
					interpretability_rating: parseInt(data.mean_rating),
					l1_l4_vector: scaledVector,
					l1: scaledVector[0],
					l2: scaledVector[1],
					l3: scaledVector[2],
					l4: scaledVector[3],
				};

				readCaptionInfo.push(caption);
			});

			let filteredData = readCaptionInfo;
			if (filterMin !== null && filterMax !== null) {
				filteredData = filteredData.filter(item => item.interpretability_rating >= filterMin && item.interpretability_rating <= filterMax);
			}

			if (sortOrder === "asc") {
				filteredData.sort((a, b) => a[sortKey] - b[sortKey]);
			} else {
				filteredData.sort((a, b) => b[sortKey] - a[sortKey]);
			}

			setCaptionInfo(filteredData);
		};

		loadData();
	}, [sortKey, sortOrder, filterMin, filterMax]);

	return (
		<Analysis
			goal="Effect of L1-L4 sentences"
			obs={[
				{
					"For captions with low interpretability (1-3):": [
						"Fairly even distribution of sentence types, i.e, no one type of sentence is more prevalant than the rest."
					]
				},
				{
					"For captions with high interpretability (4-5):": [
						"more L4 sentences than for low interpretability ones",
						"less L1 sentences than for low interpretability ones"
					]
				},
			]}
			next={[
				"Some sentence combinations appear to have higher interpretability rating than others. Find the combinations that improve interpretability."
			]}
		>
			<div className="flex flex-col h-full w-full">
				<div className="flex flex-row gap-3">
					<DropdownMenu>
						<DropdownMenuTrigger asChild>
							<Button variant="outline">Sort by: {sortKey}</Button>
						</DropdownMenuTrigger>
						<DropdownMenuContent>
							{["imageid", "interpretability_rating", "l1", "l2", "l3", "l4"].map((key) => (
								<DropdownMenuItem key={key} onClick={() => setSortKey(key as keyof CaptionInfo)}>
									{key.replace(/_/g, " ")}
								</DropdownMenuItem>
							))}
						</DropdownMenuContent>
					</DropdownMenu>

					<DropdownMenu>
						<DropdownMenuTrigger asChild>
							<Button variant="outline">Order: {sortOrder}</Button>
						</DropdownMenuTrigger>
						<DropdownMenuContent>
							<DropdownMenuItem onClick={() => setSortOrder("asc")}>Ascending</DropdownMenuItem>
							<DropdownMenuItem onClick={() => setSortOrder("desc")}>Descending</DropdownMenuItem>
						</DropdownMenuContent>
					</DropdownMenu>

					<div className="flex items-center gap-2">
						<Input
							min={1} max={5}
							type="number"
							placeholder="Min Rating"
							className="w-40"
							value={filterMin ?? ''} onChange={(e) => setFilterMin(e.target.value ? parseInt(e.target.value) : null)}
						/>
						<Input
							min={1} max={5}
							type="number"
							placeholder="Max Rating"
							className="w-40"
							value={filterMax ?? ''} onChange={(e) => setFilterMax(e.target.value ? parseInt(e.target.value) : null)}
						/>
					</div>
				</div>


				<div className="grid grid-cols-[3fr_1fr] h-full w-full">
					<div>
						<Heatmap
							data={captionInfo.map(c => ({ 'id': c.imageid, 'vectors': c.l1_l4_vector }))}
							x_cat={["L1", "L2", "L3", "L4"]}
						/>
					</div>
					<div>
						<HorizontalBar
							d={captionInfo.map(c => ({ 'category': c.imageid, 'value': c.interpretability_rating }))}
						/>
					</div>
				</div>
			</div>
		</Analysis>
	);
}

export default L1l4Effect;
