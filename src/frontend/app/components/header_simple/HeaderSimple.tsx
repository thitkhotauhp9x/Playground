import { useState } from "react";
import {
  Burger,
  Button,
  Container,
  Dialog,
  Divider,
  Drawer,
  Group,
  ScrollArea,
  TextInput,
  Text,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from "./HeaderSimple.module.css";
import { Login } from "@/app/components/login/Login";
import { Text2Audio } from "@/app/components/text2audio/Text2Audio";
import {Conversation} from "@/app/components/conversation/Conversation";
import {ActionsGrid} from "@/app/components/ActionsGrid";

const links = [
  { link: "/about", label: "Features" },
  { link: "/pricing", label: "Pricing" },
  // { link: "/text2audio", label: "Text2Audio" },
  { link: "/community", label: "Community" },
];

export function HeaderSimple() {
  const [opened, { toggle, close }] = useDisclosure(false);
  const [active, setActive] = useState(links[0].link);

  const items = links.map((link) => (
    <a
      key={link.label}
      href={link.link}
      className={classes.link}
      data-active={active === link.link || undefined}
      onClick={(event) => {
        event.preventDefault();
        setActive(link.link);
      }}
    >
      {link.label}
    </a>
  ));

  // const [openedLogin, { toggle, close }] = useDisclosure(false);

  return (
    <>
      <header className={classes.header}>
        <Container size="md" className={classes.inner}>
          <Group gap={5} visibleFrom="xs">
            {items}
          </Group>
          <Login></Login>

          <Burger
            opened={opened}
            onClick={toggle}
            hiddenFrom="xs"
            size="sm"
            aria-label="Toggle navigation"
          />
        </Container>

        <Drawer
          opened={opened}
          onClose={close}
          size="100%"
          padding="md"
          title="Navigation"
          hiddenFrom="xs"
          zIndex={1000000}
        >
          <ScrollArea h="calc(100vh - 80px" mx="-md">
            <Divider my="sm" />
            {items}
          </ScrollArea>
        </Drawer>
      </header>
      <Container>
        <Text2Audio></Text2Audio>
        <Conversation></Conversation>
        <ActionsGrid></ActionsGrid>
      </Container>
    </>
  );
}
