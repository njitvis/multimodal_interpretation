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

const KeywordDistribution = () => {
	const [captionInfo, setCaptionInfo] = useState<CaptionInfo[]>([]);
	const [sortKey, setSortKey] = useState<keyof CaptionInfo>("interpretability_rating");
	const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
	const [filterMin, setFilterMin] = useState<number | null>(null);
	const [filterMax, setFilterMax] = useState<number | null>(null);

	useEffect(() => {
		const loadData = async () => {
			const readCaptionInfo: CaptionInfo[] = [];
			await d3.csv("/data/download.csv", (data: CaptionInfoRead) => {
				const vector = data.keyword_vector
					.substring(1, data.keyword_vector.length - 1)
					.split(', ').map(vector => parseInt(vector));

				const vec_total = vector.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

				const caption: CaptionInfo = {
					chart_type: data.chart_type,
					clarity: data.clarity,
					complexity: data.complexity,
					imageid: data.image_id,
					interpretability_rating: parseInt(data.mean_rating),
					keyword_vector: vector,
					aggregation: vector[0] / vec_total,
					uncertainty: vector[1] / vec_total,
					statistics: vector[2] / vec_total,
					task: vector[3] / vec_total,
					pattern: vector[4] / vec_total,
					graphical: vector[5] / vec_total,
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
			goal="Distribution of Keywords"
			obs={[
				{
					"For low interpretability rating (1-3):": [
						"fewer aggregation keywords with higher graphical keywords.",
						"low proportion of uncertainity and task keywords.",
						"lower porportion of uncertainity keywords show higher proportion of task keywords.",
						"high proportion og graphical keywords observed."
					]
				},
				{
					"For high interpretability rating (4-5):": [
						"comparatively lower proportion of graphical keywords."
					]
				}
			]}
			next={[
				"expand keywords vocabulary for nuanced patterns."
			]}
		>
			<div className="flex flex-col h-full w-full">
				<div className="flex flex-row gap-3">
					<DropdownMenu>
						<DropdownMenuTrigger asChild>
							<Button variant="outline">Sort by: {sortKey}</Button>
						</DropdownMenuTrigger>
						<DropdownMenuContent>
							{["imageid", "interpretability_rating", "aggregation", "uncertainty", "statistics", "task", "pattern", "graphical"].map((key) => (
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
							data={captionInfo.map(c => ({ 'id': c.imageid, 'vectors': c.keyword_vector }))}
							x_cat={["aggregation", "uncertainty", "statistics", "task", "pattern", "graphical"]}
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

export default KeywordDistribution;
