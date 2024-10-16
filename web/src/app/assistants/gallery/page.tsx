import { InstantSSRAutoRefresh } from "@/components/SSRAutoRefresh";
import { WelcomeModal } from "@/components/initialSetup/welcome/WelcomeModalWrapper";
import { fetchChatData } from "@/lib/chat/fetchChatData";
import { unstable_noStore as noStore } from "next/cache";
import { redirect } from "next/navigation";
import WrappedAssistantsGallery from "./WrappedAssistantsGallery";
import { AssistantsProvider } from "@/components/context/AssisantsContext";

export default async function GalleryPage({
  searchParams,
}: {
  searchParams: { [key: string]: string };
}) {
  noStore();

  const data = await fetchChatData(searchParams);

  if ("redirect" in data) {
    redirect(data.redirect);
  }

  const {
    user,
    chatSessions,
    assistants,
    folders,
    openedFolders,
    shouldShowWelcomeModal,
    toggleSidebar,
  } = data;

  return (
    <>
      <AssistantsProvider initialAssistants={assistants}>
        {shouldShowWelcomeModal && <WelcomeModal user={user} />}

        <InstantSSRAutoRefresh />

        <WrappedAssistantsGallery
          initiallyToggled={toggleSidebar}
          chatSessions={chatSessions}
          folders={folders}
          openedFolders={openedFolders}
          user={user}
        />
      </AssistantsProvider>
    </>
  );
}
