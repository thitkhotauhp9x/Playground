"use client";

import { Container, MantineProvider } from "@mantine/core";
import "@mantine/core/styles.css";
import { Counter } from "@/app/components/counter/Counter";
import { Messages } from "@/app/components/counter/Messages";
import { HeaderSimple } from "@/app/components/header_simple/HeaderSimple";
import { FooterSimple } from "@/app/components/footer/FooterSimple";
import { GridAsymmetrical } from "@/app/components/GridAsymmetrical";
// import {Login} from "@/app/components/login/_Login";
import { RegexSearch } from "@/app/components/search/RegexSearch";
import { Pronunciation } from "@/app/components/pronunciation";
import { Text2Audio } from "@/app/components/text2audio/Text2Audio";

export default function Home() {
  return (
    <MantineProvider>
      <HeaderSimple></HeaderSimple>
      {/*<Container>*/}
      {/*  /!*  /!*    <Demo></Demo>*!/*!/*/}
      {/*  /!*  /!*<ConversationDialog></ConversationDialog>*!/*!/*/}
      {/*  /!*  /!*<Messages/>*!/*!/*/}
      {/*  /!*  /!*<Counter></Counter>*!/*!/*/}
      {/*  /!*  <RegexSearch></RegexSearch>*!/*/}
      {/*  /!*  <Pronunciation></Pronunciation>*!/*/}
      {/*  <Text2Audio></Text2Audio>*/}
      {/*</Container>*/}
      {/*<GridAsymmetrical></GridAsymmetrical>*/}
      {/*<FooterSimple></FooterSimple>*/}
    </MantineProvider>
  );
}
