import useCards, { CardQuery } from "../hooks/useCards";

interface Props {
  cardQuery: CardQuery;
}

const MainPanel = ({ cardQuery }: Props) => {
  const { data, error } = useCards(cardQuery);

  console.log(data);

  if (error) return <h1>{error}</h1>;

  return (
    <div className="container d-flex flex-wrap">
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
      <img src={"https://arkhamdb.com/bundles/cards/01016.png"}></img>
    </div>
  );
};

export default MainPanel;
