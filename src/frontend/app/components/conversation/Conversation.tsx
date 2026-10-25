import { useDisclosure } from "@mantine/hooks";
import {
  Modal,
  Button,
  Container,
} from "@mantine/core";


export function Conversation() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        fullScreen
        radius={0}
        transitionProps={{ transition: "fade", duration: 200 }}
      >
        <Container>
          Conversation
        </Container>
      </Modal>

      <Button variant="default" onClick={open}>
        Conversation
      </Button>
    </>
  );
}
