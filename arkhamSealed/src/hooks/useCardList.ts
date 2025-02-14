import { CardQuery } from "../App";
import useData from "./useData"
import { Card } from "./useCard"

export interface CardList {
    numCards: number,
    cardList: Card[]
}


const useCardList = (cardQuery : CardQuery) => {
    const params: { name?: string, cardText?: string, factions?: string } = {};

    if (cardQuery.name) {
        params.name = cardQuery.name
    }

    if (cardQuery.cardText) {
        params.cardText = cardQuery.cardText
    }

    if (cardQuery.factions && cardQuery.factions.length > 0) {
        params.factions = cardQuery.factions.join(',');
    }

    return useData<CardList>('/cards/', { params }, [cardQuery])
}

export default useCardList