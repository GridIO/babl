import { apiResponse } from "./api-response";

export class Person {
  id: number;
  url: string;
  display_name: string;
  about_me: string;
  age: number;
  height: number;
  weight: number;
  ethnicity: string;
  body_type: string;
  position: string;
  rel_status: string;
  hiv_status: string;
  hiv_test_date: string;
  images: Array<Object>;
  distance: number;
  most_recent_message: string;
  date_of_last_contact: string;
}

export class PersonResponse extends apiResponse {
  results: Person[];
}

export let Attributes = {
    'ETHNICITY': {
      'AS': 'Asian',
      'BL': 'Black',
      'LA': 'Latino',
      'ME': 'Middle Eastern',
      'MI': 'Mixed',
      'NA': 'Native American',
      'WH': 'White',
      'SA': 'South Asian',
      'OT': 'Other'
    },
    'BODY_TYPE': {
      'TO': 'Toned',
      'AV': 'Average',
      'LA': 'Large',
      'MU': 'Muscular',
      'SL': 'Slim',
      'ST': 'Stocky'
    },
    'POSITION': {
      'TO': 'Top',
      'VT': 'Vers Top',
      'VS': 'Versatile',
      'VB': 'Vers Bottom',
      'BO': 'Bottom'
    },
    'REL_STATUS': {
      'CO': 'Committed',
      'DA': 'Dating',
      'EN': 'Engaged',
      'EX': 'Exclusive',
      'MA': 'Married',
      'OR': 'Open Relationship',
      'PA': 'Partnered',
      'SI': 'Single'
    },
    'HIV_STATUS': {
      'NE': 'Negative',
      'NP': 'Negative, on PrEP',
      'PO': 'Positive',
      'PU': 'Positive, Undetectable'
    }
}
