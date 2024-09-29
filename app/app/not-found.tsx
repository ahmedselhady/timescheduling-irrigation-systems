import Link from "next/link";
import { Button } from "@mui/material";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center gap-6">
      <h2 className="text-4xl">This Page is under construction</h2>
      <Link href="/">
        <Button color="primary" variant="contained">
          Return Home
        </Button>
      </Link>
    </div>
  );
}
