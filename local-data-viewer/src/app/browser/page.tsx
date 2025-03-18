'use client';

import React, { useEffect, useState } from 'react';
import Image from 'next/image'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import data from '@/app/data';
import { Caption } from '@/types';
import DataTable from './table';
import DataCard from './card';


const Home = () => {
  const [view, setView] = useState('table'); // 'table' or 'grid'
  const [filter, setFilter] = useState(''); // Filter value
  const [selectedItem, setSelectedItem] = useState<Caption | null>(null); // Selected item for pop-up dialog
  const [formattedData, setFormattedData] = useState<Caption[]>([]);
  const [selectedAttribute, setSelectedAttribute] = useState("imageId");

  const filteredData = formattedData.filter((item) => item[selectedAttribute].toLowerCase().includes(filter.toLowerCase()));

  useEffect(() => {
    let i = 0;
    const reqData: Caption[] = []
    for (; data[i];) {
      const dataObj: Caption = {
        imageId: (data[i]["image_id"]).toString(),
        caption: data[i]["caption"],
        context: data[i]["context"],
        type: data[i]["chart_type"]
      }
      reqData.push(dataObj);
      i++;
    }
    setFormattedData(reqData);
  }, []);

  if (formattedData.length == 0) {
    return (
      <div className="flex items-center justify-center space-x-2">
        <div className="w-4 h-4 rounded-full animate-spin bg-blue-500"></div>
        <span>Loading...</span>
      </div>
    );
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <div className="flex gap-2 mb-4">
          <Select onValueChange={setSelectedAttribute}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Select Attribute" />
            </SelectTrigger>
            <SelectContent>
              {Object.keys(formattedData[0]).map((key) => (
                <SelectItem key={key} value={key} className="capitalize">{key}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Input
            type="text"
            placeholder="Filter values"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="max-w-sm"
          />
        </div>
        <div className="flex space-x-2">
          <Button onClick={() => setView('table')} variant={view === 'table' ? 'default' : 'outline'}>
            Table View
          </Button>
          <Button onClick={() => setView('grid')} variant={view === 'grid' ? 'default' : 'outline'}>
            Grid View
          </Button>
        </div>
      </div>

      {
        filteredData.length > 0 ? (
          <>
            {view === 'table' ? (
              <DataTable filteredData={filteredData} setSelectedItem={setSelectedItem} />
            ) : (
              <DataCard filteredData={filteredData} setSelectedItem={setSelectedItem} />
            )}
          </>
        ) : (
          <p>No data found.</p>
        )
      }
      {selectedItem && (
        <Dialog open={!!selectedItem} onOpenChange={() => setSelectedItem(null)}>
          <DialogContent className="w-[calc(100vw-100px)] h-[calc(100vh-100px)] max-w-none max-h-none flex">
            <div className="w-1/2 flex items-center justify-center p-4">
              <Image
                src={`/images/${selectedItem.imageId}.jpg`}
                alt={selectedItem.caption}
                className="object-contain max-w-full max-h-full"
                width={1000}
                height={1000}
              />
            </div>

            <div className="w-1/2 flex flex-col p-6 overflow-auto max-h-full">
              <DialogHeader>
                <DialogTitle>Image ID: {selectedItem.imageId}</DialogTitle>
              </DialogHeader>
              <p className="mt-10 text-lg">
                <strong>Caption:</strong> {selectedItem.caption}
              </p>
              <p className="mt-10 text-lg">
                <strong>Context:</strong> {selectedItem.context}
              </p>
            </div>
          </DialogContent>
        </Dialog>

      )}
    </div>
  );
}

export default Home;
