export interface Caption {
  imageId: string;
  caption: string;
  context: string;
  type: string;
}

export interface CaptionInfo {
  chart_type: string;
  clarity: string;
  complexity: string;
  imageid: string;
  interpretability_rating: number;
  keyword_vector?: number[];
  aggregation?: number,
  uncertainty?: number,
  statistics?: number,
  task?: number,
  pattern?: number,
  graphical?: number,
  l1_l4_vector?: number[];
  l1?: number,
  l2?: number,
  l3?: number,
  l4?: number,
}

export interface CaptionInfoRead {
  chart_type: string;
  clarity: string;
  complexity: string;
  image_id: string;
  mean_rating: string;
  keyword_cluster: string;
  keyword_vector: string;
  l1_l4_cluster: string;
  l1_l4_vector: string;
}