import { CardQuery } from "../App";
import useCycleCards from "../hooks/useCycleCards";

interface Props {
  cardQuery: CardQuery;
}

const MainPanel = ({ cardQuery }: Props) => {
  const BASE = "https://arkhamdb.com/";
  const { data, error, isLoading } = useCycleCards(cardQuery);

  console.log("data:", data);

  if (error) return <h1>{error}</h1>;

  return (
    <>
      <div className="container d-flex flex-wrap">
        {data
          .filter((card) => card.type === "investigator")
          .map((card) => (
            <img src={BASE + card.image_url}></img>
          ))}
      </div>
      <div className="container d-flex flex-wrap">
        {data
          .filter((card) => card.type !== "investigator")
          .map((card) => (
            <img src={BASE + card.image_url}></img>
          ))}
      </div>
    </>
  );
};

export default MainPanel;
