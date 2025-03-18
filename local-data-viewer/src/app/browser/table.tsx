import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Caption } from "@/types";

const DataTable = ({ filteredData, setSelectedItem }) => {
  return (
    <div className="w-full overflow-x-auto">
      <Table className="w-full">
        <TableHeader>
          <TableRow>
            {Object.keys(filteredData[0]).map((key) => (
              <TableHead key={key} className="capitalize">
                {key}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredData.map((item: Caption) => (
            <TableRow
              key={item.imageId}
              className="cursor-pointer hover:bg-gray-100"
              onClick={() => setSelectedItem(item)}
            >
              {Object.values(item).map((value, idx) => (
                <TableCell
                  key={`${item.imageId}-${idx}`}
                  className="max-w-[300px] truncate overflow-hidden text-ellipsis whitespace-nowrap"
                >
                  {value}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

export default DataTable;