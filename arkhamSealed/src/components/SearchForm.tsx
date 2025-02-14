import { FieldValues, useForm } from "react-hook-form";
import { CardQuery } from "../App";

interface Props {
  cardQuery: CardQuery;
  setQuery: (query: CardQuery) => void;
}

const SearchForm = ({ cardQuery, setQuery }: Props) => {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data: FieldValues) => {
    // Convert form data into CardQuery structure
    const query: CardQuery = {
      id: Date.now(), // Placeholder for ID, since it's not in the form
      name: data.name || "",
      cycle: "", // No cycle field in the form, so default empty
      type: "", // No type field in the form, so default empty
      factions: Object.keys(data.factions || {}).filter(
        (key) => data.factions[key] // Keep only checked factions
      ),
      cardText: data.text || "",
    };

    console.log(query);
    setQuery(query);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="mb-3">
        <label htmlFor="name" className="form-label">
          Card Name
        </label>
        <input
          {...register("name")}
          id="name"
          type="text"
          className="form-control"
        />
      </div>
      <div className="mb-3">
        <label htmlFor="text" className="form-label">
          Card Text
        </label>
        <input
          {...register("text")}
          id="text"
          type="text"
          className="form-control"
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Select Factions</label>
        <div className="form-check form-check-inline">
          {["Guardian", "Seeker", "Rogue", "Mystic", "Survivor", "Neutral"].map(
            (option) => (
              <div key={option} className="form-check form-check-inline">
                <input
                  type="checkbox"
                  className="form-check-input"
                  {...register(`factions.${option}`)} // The key is now the option name
                  value={option} // The value is the class name (e.g., "Guardian")
                />
                <label className="form-check-label">{option}</label>
              </div>
            )
          )}
        </div>
      </div>
      <button className="btn btn-primary" type="submit">
        Submit
      </button>
    </form>
  );
};

export default SearchForm;
