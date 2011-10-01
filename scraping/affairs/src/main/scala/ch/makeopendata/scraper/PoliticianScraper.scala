package ch.makeopendata.scraper

import org.htmlcleaner.HtmlCleaner
import org.htmlcleaner.TagNode
import java.net.URL
import java.net.HttpURLConnection
import com.google.gson.Gson
import java.io.FileWriter
import java.io.PrintWriter

object Crawler extends App {

  val fileName = "politicians.json"

  val gson = new Gson

  for (id <- (0 to 4047).par) {
    val politicianOption = Politician(id)
    if (politicianOption.isDefined) {
      val json = gson.toJson(politicianOption.get)
      this.synchronized {
        append(fileName, json)
        println(politicianOption.get.party + " saved")
      }
    } else {
      println(id + " discarded")
    }
  }

  def append(fileName: String, text: String) {
    val fileWriter = new FileWriter(fileName, true)
    val printWriter = new PrintWriter(fileWriter)
    printWriter.println(text)
    fileWriter.close
  }

}