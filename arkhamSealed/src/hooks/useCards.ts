import useData from "./useData"

export interface CardQuery {
    id: number;
    name: string;
}

export interface Card {
    id: number;
    name: string;
    image_url: string;
}

const useCards = (cardQuery : CardQuery) => useData<Card>('./card/', {
    params : {
        id: cardQuery.id
    }},
    [cardQuery])

export default useCards 