import {
  IconTextRecognition,
} from '@tabler/icons-react';
import {
  Modal,
  Text,
  UnstyledButton,
  useMantineTheme,
} from '@mantine/core';
import classes from './ActionsGrid.module.css';
import {useDisclosure} from "@mantine/hooks";
import MindMap from "@/app/components/mindmap/MindMap";

export function ActionsGrid() {
  const [opened, { open, close }] = useDisclosure(false);

  const theme = useMantineTheme();

  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        fullScreen
        radius={0}
        transitionProps={{ transition: "fade", duration: 200 }}
      >
        <MindMap></MindMap>
      </Modal>
      <UnstyledButton className={classes.item} onClick={open}>
        <IconTextRecognition color={theme.colors["blue"][6]} size={32} stroke={1.5} />
        <Text size="xs" mt={7}>
          {"Convert text to audio"}
        </Text>
      </UnstyledButton>
    </>
  );
}
