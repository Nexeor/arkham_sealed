import { CardQuery } from "../App";
import useData from "./useData"

export interface Card {
    type: string;
    id: number;
    name: string;
    image_url: string;
    faction: string;
}

const useCards = (cardQuery : CardQuery) => useData<Card>('./card/', {
    params : {
        id: cardQuery.id
    }},
    [cardQuery])

export default useCards 