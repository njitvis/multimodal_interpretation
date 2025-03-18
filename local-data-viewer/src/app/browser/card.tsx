import { Card, CardContent } from "@/components/ui/card";
import Image from "next/image";

const DataCard = ({ filteredData, setSelectedItem }) => {
	return (

		<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
			{filteredData.map((item: Caption) => (
				<Card key={item.imageId} className="p-4" onClick={() => setSelectedItem(item)}>
					<div className="w-64 h-64 mx-auto relative">
						<Image
							src={`/images/${item.imageId}.jpg`}
							alt={item.caption}
							layout="fill"
							objectFit="cover"
							className="rounded-md"
						/>
					</div>
					<CardContent className="mt-2 text-center">
						<p className="max-w-full line-clamp-2 overflow-hidden text-ellipsis">{item.caption}</p>
					</CardContent>
				</Card>
			))}
		</div>
	);
}

export default DataCard;