import arkhamLogo from "../assets/arkham-logo.png";
import TypeRadio from "./TypeRadio";

interface Props {
  setSelected: (selectedClass: string) => void;
  selected: string;
}

const Header = ({ setSelected, selected }: Props) => {
  return (
    <div className="d-flex justify-content-between align-items-center p-3">
      <img src={arkhamLogo} style={{ maxWidth: "200px", maxHeight: "100px" }} />
      <TypeRadio setSelected={setSelected} selected={selected} />
    </div>
  );
};

export default Header;
