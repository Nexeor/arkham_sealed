import { useState } from "react";
import { CardQuery } from "../App";
import useCycleCards from "../hooks/useCycleCards";
import ClassSelector from "./ClassSelector";

interface Props {
  cardQuery: CardQuery;
}

const MainPanel = ({ cardQuery }: Props) => {
  const BASE = "https://arkhamdb.com/";
  const { data, error } = useCycleCards(cardQuery);
  const [selectedFaction, setSelectedFaction] = useState("");

  console.log("data:", data);
  console.log(selectedFaction);
  if (error) return <h1>{error}</h1>;

  return (
    <>
      <ClassSelector onSelect={setSelectedFaction} />
      <div className="container d-flex flex-wrap">
        {data
          .filter((card) => card.type === "investigator")
          .filter(
            (card) => selectedFaction === "" || card.faction === selectedFaction
          )
          .map((card) => (
            <img src={BASE + card.image_url}></img>
          ))}
      </div>
      <div className="container d-flex flex-wrap">
        {data
          .filter((card) => card.type !== "investigator")
          .filter(
            (card) => selectedFaction === "" || card.faction === selectedFaction
          )
          .map((card) => (
            <img src={BASE + card.image_url}></img>
          ))}
      </div>
    </>
  );
};

export default MainPanel;
