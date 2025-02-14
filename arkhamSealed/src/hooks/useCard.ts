import { CardQuery } from "../App";
import useData from "./useData"

export interface Card {
    type: string;
    id: number;
    name: string;
    image_url: string;
    faction: string;
    cardText: string;
}

const useCard = (cardQuery : CardQuery) => useData<Card>('./card/', {
    params : {
        id: cardQuery.id
    }},
    [cardQuery])

export default useCard