import { FieldValues, useForm } from "react-hook-form";

const SearchForm = () => {
  const { register, handleSubmit } = useForm();
  const onSubmit = (data: FieldValues) => console.log(data);

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
      {/* PLACEHOLDER, MUST BE REPLACED WITH MULTI-SELECT*/}
      <div className="mb-3">
        <label htmlFor="category" className="form-label">
          Traits
        </label>
        <select {...register("category")} id="category" className="form-select">
          <option value="">Select Traits</option>
          <option value="1">One</option>
          <option value="2">Two</option>
          <option value="3">Three</option>
          <option value="4">Four</option>
          <option value="5">Five</option>
        </select>
      </div>
      <div className="mb-3">
        <label className="form-label">Select Factions</label>
        <div className="form-check form-check-inline">
          {["Guardian", "Seeker", "Rogue", "Mystic", "Survivor", "Neutral"].map(
            (option, index) => (
              <div key={index} className="form-check form-check-inline">
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
