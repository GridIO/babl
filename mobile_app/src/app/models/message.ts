import { apiResponse } from "./api-response";

export class Message {
  id: number;
  sender: number;
  recipient: number;
  message_type: string;
  sender_content: string;
  recipient_content: string;
  image: string;
  sent_at: string;
  read_at: string;
}

export class MessageResponse extends apiResponse {
  results: Message[];
}
