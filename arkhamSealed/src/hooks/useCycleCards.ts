import { CardQuery } from "../App";
import { Card } from "./useCard";
import useData from "./useData"

const useCycleCards = (cardQuery : CardQuery) => useData<Card>('./cards/cycle', {
    params : {
        cycle_code: cardQuery.cycle
    }},
    [cardQuery])

export default useCycleCards 