import { CardQuery } from "../App";
import useCardList from "../hooks/useCardList";
import SearchForm from "./SearchForm";

interface Props {
  cardQuery: CardQuery;
  setQuery: (query: CardQuery) => void;
  selectedType: string;
}

type cardType = {
  [key: string]: string[];
};

const typeMap: cardType = {
  Investigator: ["investigator"],
  "Player Cards": ["asset", "skill", "event"],
  Mythos: ["treachery"],
};

const MainPanel = ({ cardQuery, setQuery, selectedType }: Props) => {
  const BASE = "https://arkhamdb.com/";
  const { data, error } = useCardList(cardQuery);
  console.log("data: ", data);
  // const [selectedFaction, setSelectedFaction] = useState("");

  if (error) return <h1>{error}</h1>;

  const filteredData =
    selectedType !== "All"
      ? data.filter((card) => typeMap[selectedType]?.includes(card.type))
      : data;

  return (
    <>
      <SearchForm setQuery={setQuery} />
      <div className="container d-flex flex-wrap">
        {filteredData
          .filter((card) => card.type === "investigator")
          .map((card) => (
            <img src={BASE + card.image_url}></img>
          ))}
      </div>
      <div className="container d-flex flex-wrap">
        {filteredData
          .filter((card) => card.type !== "investigator")
          .map((card) => (
            <img src={BASE + card.image_url}></img>
          ))}
      </div>
    </>
  );
};

export default MainPanel;
